from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from datetime import datetime

from core.database import AsyncSessionLocal
from service.APIReq import APIReq

def job_error_listener(event):
    print(f"###[Error!]스케쥴 작업 실패. Error: {event.exception}")
    print(f"작업 ID: {event.job_id}")
    print(f"작업 실행 시간: {event.scheduled_run_time}")

def job_executed_listener(event):
    print(f"###스케쥴 작업 성공!###")
    print(f"작업 ID: {event.job_id}")
    print(f"작업 실행 시간: {event.scheduled_run_time}")
    
async def getData():
    import asyncio
    try:
        print("###Scheduler Start###")
        async with AsyncSessionLocal() as db:
            try:
                await APIReq.get("station", db)
                await APIReq.get("pollution", db)
                await db.commit()
            except Exception as e:
                await db.rollback()
                print(f"데이터 수집 중 오류 발생: {e}")
                raise e
    except asyncio.CancelledError:
        print("서버 종료로 인한 작업 취소")
        raise

scheduler = AsyncIOScheduler()
scheduler.add_listener(job_error_listener, EVENT_JOB_ERROR)
scheduler.add_listener(job_executed_listener, EVENT_JOB_EXECUTED)


scheduler.add_job(
    getData,
    'date',
    run_date=datetime.now(),
    misfire_grace_time=None,
    id='init_run'
)

scheduler.add_job(
    getData, 
    "cron", 
    minute="10,20,40",
    max_instances=1,
    misfire_grace_time=900,
    id='periodic_run'
)

scheduler.print_jobs()