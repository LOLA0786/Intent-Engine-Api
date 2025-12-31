import requests
import os

OPA_URL = os.getenv("OPA_URL", "http://localhost:8181/v1/data/uaal/allow")

def opa_allow(intent: dict) -> bool:
    resp = requests.post(
        OPA_URL,
        json={"input": intent},
        timeout=2
    )
    resp.raise_for_status()
    return resp.json()["result"] is True
