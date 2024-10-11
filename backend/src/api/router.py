import os.path
from datetime import datetime

import aiofiles
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    File,
    HTTPException,
    Path,
    Query,
    UploadFile,
    status,
)
from src.utils.process_video import process_video
from yolo.tracking.tracking import Tracker

router = APIRouter(prefix='/api/v0', tags=['Video Processing'])

tracker = Tracker('../../yolo/inputs/yolo11n.pt')


def get_now_timestamp():
    return datetime.now().replace(microsecond=0).timestamp()


@router.get(
    "/processed/video/{video_id}",
    response_description="Upload new video",
    status_code=status.HTTP_201_CREATED,
)
async def download_processed_video(
    video_path: str = Path(),
) -> dict:
    try:
        filename = video.filename
        async with aiofiles.open(filename, 'wb') as f:
            while contents := await video.read(1024 * 1024):
                await f.write(contents)
    except Exception:
        return {'message': 'There was an error uploading the file'}

    return {'message': f"Successfuly uploaded {filename}"}


@router.post(
    "/raw/video/upload",
    response_description="Upload new video",
    status_code=status.HTTP_201_CREATED,
)
async def upload_new_video(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
) -> dict:
    try:
        filename: str = video.filename
        video_path: str = os.path.join('database/raw', filename)
        async with aiofiles.open(filename, 'wb') as f:
            while contents := await video.read(1024 * 1024):
                await f.write(contents)
    except Exception:
        return {'message': 'There was an error uploading the file'}

    background_tasks.add_task(process_video, process_video, video_path)
    return {'message': f"Successfuly uploaded {filename}"}
