import os
import threading
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from stop import Stop

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

from main import get_data

POLL_INTERVAL = 60  # seconds
STOP_CODE = os.getenv("TRANSIT_STOP_CODE") #REQUIRED: adding code from env soon
ID = os.getenv("TRANSIT_AGENCY_ID") #REQUIRED: adding id from env soon

cache_lock = threading.Lock()
stop_event = threading.Event()

cached_stop: Stop | None = None
cached_fetched_at: datetime | None = None

def poll_transit_data():
    global cached_stop, cached_fetched_at
    while not stop_event.is_set():
        try:
            stop = get_data(ID, STOP_CODE)
            fetched_at = datetime.now(timezone.utc)

            with cache_lock:
                cached_stop = stop
                cached_fetched_at = fetched_at
        except Exception as e:
            print(f"Error polling transit data: {e}")
            pass
        stop_event.wait(POLL_INTERVAL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not ID or not STOP_CODE:
        raise ValueError("Agency ID or Stop Code not found. Set the TRANSIT_AGENCY_ID and TRANSIT_STOP_CODE environment variables in the .env file.")
    stop_event.clear()

    worker = threading.Thread(target=poll_transit_data, name="transit-poller", daemon=True)
    worker.start()

    yield

    stop_event.set()
    worker.join(timeout=25)

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    with cache_lock:
        stop = cached_stop
        fetched_at = cached_fetched_at

    if stop is None:
        raise HTTPException(status_code=503, detail="Transit data not available yet. Please try again later.")
    return jsonable_encoder({
        "data": stop,
        "last updated": fetched_at,
    })

if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)