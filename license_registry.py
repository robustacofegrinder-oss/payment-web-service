import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY_FILE = Path(__file__).parent / "licenses.json"

def load_registry():
    if not REGISTRY_FILE.exists():
        return []

    return json.loads(
        REGISTRY_FILE.read_text(encoding="utf-8")
    )

def save_registry(records):
    REGISTRY_FILE.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def add_license(key, customer=""):
    records = load_registry()

    record = {
        "key": key,
        "customer": customer,
        "device_id": None,
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    records.append(record)
    save_registry(records)
    return record


def activate_license(key, device_id):
    records = load_registry()
    for record in records:
        if record.get("key") == key:
            if not record.get("active"):
                return False
            if record.get("device_id") is None:
                record["device_id"] = device_id
                save_registry(records)
                return True
            return record.get("device_id") == device_id
    return False
