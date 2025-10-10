from datetime import datetime, timezone


def default_timestamp(tz: timezone = timezone.utc) -> float:
    return datetime.now(tz).timestamp()
