import os
import time

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def log(msg: str, script_name: str = "general"):
    """Print to console and write to log file with UTF-8 encoding."""
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)

    logfile = os.path.join(LOG_DIR, f"{script_name}.log")
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(line + "\n")
