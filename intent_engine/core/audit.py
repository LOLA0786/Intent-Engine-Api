import sqlite3
import json
from datetime import datetime

DB_PATH = "uaal_audit.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            agent_id TEXT,
            policy TEXT,
            intent TEXT,
            decision TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_decision(evidence_id, intent, decision):
    payload = intent.get("payload", {})
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO audit_log VALUES (?, ?, ?, ?, ?, ?)",
        (
            evidence_id,
            datetime.utcnow().isoformat(),
            payload.get("agent_id"),
            ",".join(decision.get("violations", [])),
            json.dumps(intent),
            json.dumps(decision),
        )
    )
    conn.commit()
    conn.close()

def get_decision(evidence_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM audit_log WHERE id = ?", (evidence_id,))
    row = c.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "evidence_id": row[0],
        "timestamp": row[1],
        "agent_id": row[2],
        "policy": row[3],
        "intent": json.loads(row[4]),
        "decision": json.loads(row[5]),
    }

def query_audit(agent_id=None, since=None, until=None, policy=None):
    q = "SELECT * FROM audit_log WHERE 1=1"
    args = []

    if agent_id:
        q += " AND agent_id = ?"
        args.append(agent_id)

    if policy:
        q += " AND policy LIKE ?"
        args.append(f"%{policy}%")

    if since:
        q += " AND timestamp >= ?"
        args.append(since)

    if until:
        q += " AND timestamp <= ?"
        args.append(until)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(q, args)
    rows = c.fetchall()
    conn.close()

    return [
        {
            "evidence_id": r[0],
            "timestamp": r[1],
            "agent_id": r[2],
            "policy": r[3],
        }
        for r in rows
    ]
