from fastapi import APIRouter
import logging
from datetime import datetime

router = APIRouter()

event_logger = logging.getLogger("events")

if not event_logger.handlers:
    handler = logging.FileHandler("logs/events.log")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    handler.setFormatter(formatter)
    event_logger.addHandler(handler)
    event_logger.setLevel(logging.INFO)


@router.post("/webhook")
def webhook(payload: dict):

    source = payload.get("source", "unknown")
    event = payload.get("event", "unknown")
    data = payload.get("data", {})

    event_logger.info(
        f"EVENT | source={source} | event={event} | data={data}"
    )

    return {
        "status": "received",
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "event": event,
        "processed": True
    }