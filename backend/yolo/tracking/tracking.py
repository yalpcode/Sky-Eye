import base64
import cv2
import numpy as np

from collections import defaultdict
from datetime import datetime
from ultralytics import YOLO
from ultralytics.engine.results import Boxes

from tracker import BOTSORTArgs, BOTSORTv2

class TrackedObject:
    MAX_POINTS = 90

    def __init__(self):
        self._tracked_points = []
        self.bboxes_norm = []
        self.predicted_types = defaultdict(int)
        self.first_detection = None
        self.last_detection = None
        self.cropped_frame = None

    def detect(self):
        if self.first_detection is None:
            self.first_detection = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.last_detection = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    @property
    def predicted_position(self):
        if len(self._tracked_points) < 3:
            return np.array([]).astype(np.int32)
        points_array = np.array(self._tracked_points[-16:])
        x_differences = np.diff(points_array[:, 0])
        y_differences = np.diff(points_array[:, 1])
        avg_x_diff = np.mean(x_differences) * 10
        avg_y_diff = np.mean(y_differences) * 10
        last_x = points_array[-1, 0]
        last_y = points_array[-1, 1]
        predicted_x = [last_x + avg_x_diff * point for point in range(1, 4)]
        predicted_y = [last_y + avg_y_diff * point for point in range(1, 4)]
        return np.column_stack((predicted_x, predicted_y)).astype(np.int32)

    @property
    def type(self):
        return max(self.predicted_types.keys(), key=lambda x: self.predicted_types[x])

    @property
    def points(self) -> np.ndarray:
        return np.hstack(self._tracked_points).astype(np.int32).reshape((-1, 1, 2))

    @points.setter
    def points(self, value: tuple[float, float]):
        if len(self._tracked_points) > self.MAX_POINTS:
            self._tracked_points.pop(0)
        self._tracked_points.append(value)

    @classmethod
    def set_max_points_count(cls, value):
        cls.MAX_POINTS = value

    def save(self, path):
        cv2.imwrite(path, self.cropped_frame)

    def json(self, *, send_frame: bool = False):
        return {
            "class": self.type,
            "bboxn": self.bboxes_norm,
            "points": self.points.tolist(),
            "cropped_frame": base64.encodebytes(
                b"" if not send_frame else cv2.imencode('.jpg', self.cropped_frame)[1].tobytes()
            ).decode(),
            "predicted_position": self.predicted_position.tolist(),
        }

    def __str__(self):
        return f"({self.first_detection}) - ({self.last_detection}): {self.type}(count={len(self.points)}) "

    def __len__(self):
        if not self._tracked_points:
            return 0
        return sum(self.predicted_types.values())

    def __repr__(self):
        return f"TrackedObject<{self.type}>"


class Tracker(object):
    FRAMES_COUNT = 10

    # VISUALIZE
    VERBOSE = False
    SHOW_PREDS = True
    SAVE = False

    def __init__(self, weights_path: str) -> None:
        self.model = YOLO(weights_path)
        self.tracked_objects = defaultdict(lambda: TrackedObject())
        self.custom_tracker = BOTSORTv2(BOTSORTArgs())

    def load_model(self, weights_path: str) -> None:
        self.model = YOLO(weights_path)

    def track_next_frame(self, frame: np.array) -> dict:
        results = self.model.predict(frame, verbose=self.VERBOSE, classes=[0, 2, 3, 6, 7])
        # print(results[0].boxes.shape)
        if results[0].boxes.shape[0] == 0:
            if self.SHOW_PREDS:
                cv2.imshow("YOLOv8 Tracking", frame)
            return {
                "processed_frame": base64.encodebytes(cv2.imencode('.jpg', frame)[1].tobytes()),
                "bojects": []
            }
        # print(results[0].boxes)
        objects = self.custom_tracker.update(results[0].boxes, frame)
        # print(results[0].boxes)
        if objects.shape[0] == 0:
            if self.SHOW_PREDS:
                cv2.imshow("YOLOv8 Tracking", frame)
            return {"processed_frame": base64.encodebytes(cv2.imencode('.jpg', frame)[1].tobytes()), "bojects": []}

        boxes = Boxes(objects[:, :-1], frame.shape)
        names = results[0].names
        track_ids = boxes.id.tolist()
        # print(track_ids, boxes)
        annotated_frame = results[0].plot()
        for box, track_id, name in zip(boxes, track_ids, names):
            x, y, w, h = box.xywh[0]
            cls = box.cls
            track = self.tracked_objects[track_id]
            track.detect()
            if track.cropped_frame is None:
                track.cropped_frame = self.crop_image_with_bbox(frame, map(float, box.xywhn[0]))
            track.predicted_types[results[0].names[int(cls)]] += 1
            track.points = (float(x), float(y))
            track.bboxes_norm = tuple(map(float, box.xywhn[0]))

            cv2.polylines(
                annotated_frame, [track.points], isClosed=False, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA
            )
            predicted_position = track.predicted_position
            if predicted_position.shape[0] != 0:
                cv2.polylines(
                    annotated_frame,
                    [track.predicted_position],
                    isClosed=False,
                    color=(255, 0, 0),
                    thickness=2,
                    lineType=cv2.LINE_AA,
                )
            if self.SHOW_PREDS:
                cv2.imshow("YOLOv8 Tracking", annotated_frame)
        return {
            "processed_frame": "",
            "objects": [self.tracked_objects[track_id].json(send_frame=True) for track_id in track_ids],
        }

        # return [self.tracked_objects[track_id] for track_id in track_ids]

    def track_video(self, video: str | cv2.VideoCapture) -> None:
        if isinstance(video, str):
            video = cv2.VideoCapture(video)
        while video.isOpened():
            success, frame = video.read()

            if success:
                self.track_next_frame(frame)
                # breakpoint()
                if self.SHOW_PREDS:
                    if cv2.waitKey(1) & 0xFF in [ord("q"), 27]:
                        break
            else:
                break
        if self.SHOW_PREDS:
            cv2.destroyAllWindows()

    def get_objects(self):
        return {
            key: self.tracked_objects[key]
            for key in filter(lambda x: len(self.tracked_objects.get(x)) > self.FRAMES_COUNT, self.tracked_objects)
        }

    @staticmethod
    def crop_image_with_bbox(image, bbox):
        original_height, original_width = image.shape[:2]

        x_center, y_center, w, h = bbox

        x_center = int(x_center * original_width)
        y_center = int(y_center * original_height)
        w = int(w * original_width)
        h = int(h * original_height)

        x = int(x_center - w / 2)
        y = int(y_center - h / 2)

        cropped_image = image[y : y + h, x : x + w]

        return cropped_image


if __name__ == "__main__":
    tracker = Tracker("latest_yolo.pt")
    tracker.SHOW_PREDS = True
    tracker.SAVE = False
    try:
        tracker.track_video("14052021_(t40).mp4")
    except KeyboardInterrupt:
        breakpoint()
    for num, i in enumerate(tracker.get_objects().values()):
        print(i)
        # i.save(f"{num}.jpg")
