# import cv2
#
# processed_videos = {}  #  FIXME: type: list
#
#
# def process_video(video_path: str):
#     # todo: process video
#     # todo: save result into database/processed/filename.resolution
#     cap = cv2.VideoCapture(video_path)
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if ret:
#             yield frame
#             # FIXME: here can be the function tracker.track_next_frame(frame) returns a dict with prediction data.
#             # FIXME: however, fixing this is not part of my responsibilities in the backend.
#             # FIXME: but i can suggest this:
#
#             # TODO: frame_data = tracker.track_next_frame(frame)
#             # TODO: processed_videos.append(frame_data)
