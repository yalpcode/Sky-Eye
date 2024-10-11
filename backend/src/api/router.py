import random
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import asyncio
from fastapi import BackgroundTasks, APIRouter, Body, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
# from src.schemas import OptimizationInSchema, OptimizationOutSchema

router = APIRouter(prefix="/api/v0", tags=['Optuna'])

executor = ThreadPoolExecutor()


def get_now_timestamp():
    return datetime.now().replace(microsecond=0).timestamp()


@router.get(
    "/optimizations",
    response_description="Get all optimizations",
    status_code=status.HTTP_200_OK,
)
async def api_get_raw_reports(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> list:
    """
    Getting a list of optimizations
    Args:
        limit: What number of optimizations should be returned
        offset: What number of optimizations should be skipped before
        db: Mongo DB

    Returns:
        list of optimizations in the collection
    """
    return await db.optimization.find().skip(offset).to_list(length=limit)


def worker(config):
    tuner = Tuner(jsonable_encoder(config), optimization=config.name)
    tuner.fit()



@router.post(
    "/optimizations/run",
    response_description="Run new optimization",
    status_code=status.HTTP_201_CREATED,
)
async def api_create_optimization(
    background_tasks: BackgroundTasks,
    # config: OptimizationInSchema = Body(...),
) -> dict:
    """
    Run new optimization
    Args:
        background_tasks: Background tasks
        config: Experiment parameters
        db: Mongo DB

    Returns:
        The created optimization
    """
    if await db.optimization.find_one({'name': config.name}) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'status': 'error',
                'details': f"Optimization `{config.name}` is already exists!",
            },
        )
    background_tasks.add_task(executor.submit, worker, config)

    result = await db.optimization.insert_one(
        {
            'name': config.name,
            'state': {
                'trial': 0
            },
            'tuner': dict(config.tuner),
            'metadata': dict(config.metadata),
            'created_at': get_now_timestamp(),
        }
    )
    optimization = await db.optimization.find_one(result.inserted_id)
    return optimization


# @router.get(
#     "/optimization/stats",
#     response_description="Get stats for all reports",
#     status_code=status.HTTP_201_CREATED,
# )
# async def api_get_report_stats(
#     product: str = Query(...),
#     db: AsyncIOMotorCollection = Depends(get_database),
# ) -> Stats:
#     """
#     Get stats of uploaded reports
#     Args:
#         product: Search the reports with this product
#         db: Mongo DB
#
#     Returns:
#         Stats (count of uploaded reports)
#     """
#     raw_reports_count = await db.raw_report.count_documents({"metadata.product": product})
#     stats = {'raw_reports_count': raw_reports_count}
#     return stats
