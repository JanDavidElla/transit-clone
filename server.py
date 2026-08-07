import os
import threading
from html import escape
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from stop import Stop
from zoneinfo import ZoneInfo

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from main import get_data

POLL_INTERVAL = float(os.getenv("POLL_INTERVAL") or 10) # seconds
STOP_CODE = os.getenv("TRANSIT_STOP_CODE") #REQUIRED: adding code from env soon
ID = os.getenv("TRANSIT_AGENCY_ID") #REQUIRED: adding id from env soon
TIME_ZONE = ZoneInfo(os.getenv("LOCAL_TIMEZONE") or "America/Los_Angeles")

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
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def root():
    with cache_lock:
        stop = cached_stop
        fetched_at = cached_fetched_at

    template_path = os.path.join(STATIC_DIR, "index.html")
    with open(template_path, encoding="utf-8") as template_file:
        page = template_file.read()

    if stop is None:
        stop_id = STOP_CODE or "-"
        operator_id = ID or "-"
        updated_at = "waiting for data"
        arrival_rows = '<p class="empty">Arrival information is loading. This page will refresh automatically.</p>'
    else:
        stop_id = stop.stop_id
        operator_id = stop.operator_id
        updated_at = fetched_at.astimezone(TIME_ZONE).strftime("%I:%M %p") if fetched_at else "just now"
        cards = []

        for prediction in stop.predictions:
            times = []
            for arrival_time in prediction.arrival_times:
                minutes = max(0, round((arrival_time - datetime.now(timezone.utc)).total_seconds() / 60))
                label = "Due now" if minutes == 0 else f"{minutes} min"
                times.append(
                    f'<span><strong>{label}</strong><small>{arrival_time.astimezone(TIME_ZONE).strftime("%I:%M %p")}</small></span>'
                )

            cards.append(
                '<article class="arrival">'
                f'<span class="route">{escape(prediction.route)}</span>'
                f'<div class="times">{"".join(times)}</div>'
                '</article>'
            )

        arrival_rows = "".join(cards) or '<p class="empty">No upcoming arrivals right now.</p>'

    page = page.replace("{{STOP_ID}}", escape(stop_id))
    page = page.replace("{{OPERATOR_ID}}", escape(operator_id))
    page = page.replace("{{UPDATED_AT}}", escape(updated_at))
    page = page.replace("{{ARRIVAL_ROWS}}", arrival_rows)
    return HTMLResponse(page)

@app.get("/api/transit")
def transit_data():
    with cache_lock:
        stop = cached_stop
        fetched_at = cached_fetched_at

    if stop is None:
        raise HTTPException(status_code=503, detail="Transit data not available yet. Please try again later.")
    return jsonable_encoder({
        "data": stop,
        "last_updated": fetched_at,
    })

if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)
