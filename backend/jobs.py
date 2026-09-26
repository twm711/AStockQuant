import asyncio
from datetime import datetime, timezone
from .storage import init_db

def job_status(name):
    return {'job':name,'status':'queued','created_at':datetime.now(timezone.utc).isoformat()}
async def run_once():
    return init_db()
