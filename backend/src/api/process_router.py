import base64
import os
import traceback
from datetime import datetime
from io import BytesIO

import numpy as np
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse, Response, StreamingResponse
from PIL import Image
from yolo.tracking.tracking import Tracker

router = APIRouter(prefix='/api/v0', tags=['Video Processing'])

print(os.path.dirname(__file__))
tracker = Tracker(weights_path=os.path.join(os.path.dirname(__file__), '../../yolo/inputs/latest_yolo.pt'))
tracker.SHOW_PREDS = False


def get_now_timestamp():
    return datetime.now().replace(microsecond=0).timestamp()


# @router.get(
#     "/video/processed/{video_id}",
#     response_description="Upload new video",
#     status_code=status.HTTP_201_CREATED,
# )
# async def download_processed_video(
#     video_path: str = Path(),
# ) -> dict:
#     try:
#         filename = video.filename
#         async with aiofiles.open(filename, 'wb') as f:
#             while contents := await video.read(1024 * 1024):
#                 await f.write(contents)
#     except Exception:
#         return {'message': 'There was an error uploading the file'}
#
#     return {'message': f"Successfuly uploaded {filename}"}
#
#
# @router.post(
#     "/video/raw/upload",
#     response_description="Upload new video",
#     status_code=status.HTTP_201_CREATED,
# )
# async def upload_new_video(
#     background_tasks: BackgroundTasks,
#     video: UploadFile = File(...),
# ) -> dict:
#     try:
#         filename: str = video.filename
#         video_path: str = os.path.join('database/raw', filename)
#         async with aiofiles.open(filename, 'wb') as f:
#             while contents := await video.read(1024 * 1024):
#                 await f.write(contents)
#     except Exception:
#         return {'message': 'There was an error uploading the file'}
#
#     background_tasks.add_task(process_video, process_video, video_path)
#     return {'message': f"Successfuly uploaded {filename}"}


@router.post(
    "/video/frame/detect",
    response_description="Detect objects per frame",
    status_code=status.HTTP_201_CREATED,
)
async def detect_objects_per_frames(frame: UploadFile = File(...)) -> Response:
    print(frame.content_type)
    if frame.content_type not in ('image/jpeg', 'image/jpg', 'image/png'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid document type. Available types: image/jpg, image/png',
        )
    try:
        print('we here')
        frame_bytes = await frame.read()
        frame_numpy = np.array(Image.open(BytesIO(frame_bytes)))
    except Exception as ex:
        print('we here', traceback.print_exc())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid document type. Reading error',
        )
    # try:
    # print('frame_numpy', frame_numpy)
    # print('frame_numpy shape', frame_numpy.shape)
    fragment_processed = tracker.track_next_frame(frame_numpy)
    # print('fragment_processed', fragment_processed)

    # BytesIO(fragment_processed['processed_frame'])
    image_bytes: bytes = fragment_processed['processed_frame']
    # except Exception:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail='Processing error',
    #     )
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    return JSONResponse({"image": base64_image})
