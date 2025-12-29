from fastapi import FastAPI, Header
import hashlib
import json
import time

app = FastAPI(title="UAAL Multi-Domain Demo API")

@app.post("/test")
def test(payload: dict, x_uaal_mode: str = Header(default="shadow")):
    inp = payload.get("input", {})
    domain = inp.get("domain")

    risks = []

    # --------------------
    # MEDICAL POLICIES
    # --------------------
    if domain == "healthcare":
        try:
            if inp["patient"]["age"] < 18 and inp["treatment"]["dosage_mg"] >= 500:
                risks.append("PEDIATRIC_DOSAGE_MISMATCH")

            if not inp["patient"]["consent"]:
                risks.append("MISSING_PATIENT_CONSENT")

            if inp["diagnosis"]["confidence"] < 0.7:
                risks.append("LOW_DIAGNOSTIC_CONFIDENCE")
        except KeyError as e:
            risks.append(f"SCHEMA_MISMATCH:{str(e)}")

    # --------------------
    # FINTECH POLICIES
    # --------------------
    elif domain == "fintech":
        try:
            if inp.get("amount", 0) >= 200000:
                risks.append("HIGH_VALUE_TRANSFER")

            if inp.get("new_beneficiary") is True:
                risks.append("NEW_BENEFICIARY")
        except KeyError as e:
            risks.append(f"SCHEMA_MISMATCH:{str(e)}")

    else:
        risks.append("UNKNOWN_DOMAIN")

    # --------------------
    # ENFORCEMENT
    # --------------------
    if x_uaal_mode == "enforce" and risks:
        evidence_hash = hashlib.sha256(
            (json.dumps(inp, sort_keys=True) + str(time.time())).encode()
        ).hexdigest()

        return {
            "allowed": False,
            "decision": "BLOCK",
            "reason": "Unsafe intent",
            "domain": domain,
            "violations": risks,
            "policy_version": f"{domain.upper()}_v1.0",
            "evidence": {
                "hash": evidence_hash,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }

    return {
        "allowed": True,
        "mode": x_uaal_mode,
        "domain": domain,
        "observed_risks": risks,
        "policy_version": f"{domain.upper()}_v1.0"
    }
