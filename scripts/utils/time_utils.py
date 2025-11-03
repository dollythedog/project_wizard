import re
from datetime import datetime, timezone, timedelta

# Accepts many ISO8601 variations (with or without fractional seconds, with Z or ±hh[:mm])
ISO_LIKE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})"
    r"[T ]"
    r"(\d{2}):(\d{2}):(\d{2})(\.\d{1,6})?"
    r"(Z|[+\-]\d{2}:\d{2}|[+\-]\d{2}\d{2}|[+\-]\d{2})?$"
)

def now_utc_z() -> str:
    """Return current time as UTC with trailing Z."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def normalize_to_utc_z(ts: str) -> str:
    """
    Accept 'ISO-ish' timestamp (e.g., 2025-09-28T12:34:56-05:00, 2025-09-28 12:34:56Z,
    2025-09-28T12:34:56.123456+02) and return strict UTC '...Z'.
    Raises ValueError if parsing fails.
    """
    if not isinstance(ts, str) or not ISO_LIKE.match(ts):
        raise ValueError(f"Not ISO-like: {ts!r}")

    s = ts.strip().replace(" ", "T")
    # Handle 'Z' quickly
    if s.endswith("Z"):
        # Normalize precision to seconds (drop fractional, keep hh:mm:ss)
        base = s[:-1]
        if "." in base:
            base = base.split(".")[0]
        # base has no timezone now; interpret as UTC already
        try:
            dt = datetime.fromisoformat(base).replace(tzinfo=timezone.utc)
        except ValueError:
            # Some Python builds require explicit seconds; retry with lenient split:
            ymd, hms = base.split("T")
            hh, mm, ss = hms.split(":")
            dt = datetime(int(ymd[0:4]), int(ymd[5:7]), int(ymd[8:10]),
                          int(hh), int(mm), int(ss), tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Replace bare ±HH or ±HHMM into ±HH:MM for fromisoformat
    # e.g., +02 -> +02:00; +0200 -> +02:00
    if re.search(r"[+\-]\d{2}$", s):
        s = s + ":00"
    elif re.search(r"[+\-]\d{4}$", s):
        s = s[:-2] + ":" + s[-2:]

    # Drop fractional seconds to seconds precision for consistency
    if "." in s:
        left, right = s.split(".", 1)
        # Remove timezone from right part if present
        tz = ""
        if "+" in right:
            frac, tz = right.split("+", 1)
            tz = "+" + tz
        elif "-" in right:
            frac, tz = right.split("-", 1)
            tz = "-" + tz
        elif "Z" in right:
            frac, tz = right.split("Z", 1)
            tz = "Z"
        else:
            frac = right
        s = left + tz  # drop fractional

    # Convert to aware datetime
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        # Treat naive as UTC if no tz given
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")