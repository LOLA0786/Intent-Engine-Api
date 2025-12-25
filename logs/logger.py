import json
import time
import os

LOG_PATH = "logs/routing.log"

def log_routing(event: dict):
    os.makedirs("logs", exist_ok=True)
    event["timestamp"] = time.time()

    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")
