from datetime import datetime, timezone
from pathlib import Path
import json
import secrets

ORDERS_FILE = Path(__file__).with_name("payment_orders.json")

def create_order(amount_usdt):
    order_id = "ORD-" + secrets.token_hex(5).upper()
    order = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "order_id": order_id,
        "amount_usdt": float(amount_usdt),
        "currency": "USDT",
        "network": "TRC-20",
        "status": "PENDING",
    }
    orders = []
    if ORDERS_FILE.exists():
        try:
            orders = json.loads(ORDERS_FILE.read_text(encoding="utf-8"))
        except Exception:
            orders = []
    orders.append(order)
    ORDERS_FILE.write_text(json.dumps(orders, indent=2, ensure_ascii=False), encoding="utf-8")
    return order

def get_orders():
    if not ORDERS_FILE.exists():
        return []
    try:
        return json.loads(ORDERS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


if __name__ == "__main__":
    print("Payment order module ready.")

def update_order_status(order_id, status):
    orders = get_orders()
    for order in orders:
        if order.get("order_id") == order_id:
            order["status"] = status
            ORDERS_FILE.write_text(json.dumps(orders, indent=2, ensure_ascii=False), encoding="utf-8")
            return order
    return None

def update_order_status(order_id, status):
    orders = get_orders()
    for order in orders:
        if order.get("order_id") == order_id:
            order["status"] = status
            ORDERS_FILE.write_text(json.dumps(orders, indent=2, ensure_ascii=False), encoding="utf-8")
            return order
    return None

def verify_order_payment(order_id):
    from datetime import datetime

    from payment_verifier import find_payment

    orders = get_orders()
    target = None

    for order in orders:
        if order.get("order_id") == order_id:
            target = order
            break

    if target is None:
        return None

    if target.get("status") == "PAID":
        return target

    used_ids = {
        order.get("transaction_id")
        for order in orders
        if order.get("transaction_id")
    }

    created_after = None
    if target.get("created_at"):
        created_after = int(
            datetime.fromisoformat(
                target["created_at"].replace("Z", "+00:00")
            ).timestamp() * 1000
        )

    payment = find_payment(
        target.get("amount_usdt"),
        used_ids=used_ids,
        created_after=created_after
    )

    if payment is None:
        return target

    target["status"] = "PAID"
    target["transaction_id"] = payment["transaction_id"]
    target["paid_at"] = datetime.now(timezone.utc).isoformat()

    ORDERS_FILE.write_text(
        json.dumps(orders, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    return target


def attach_license(order_id, license_key):
    orders = get_orders()

    for order in orders:
        if order.get("order_id") == order_id:
            order["license_key"] = license_key

            ORDERS_FILE.write_text(
                json.dumps(orders, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            return order

    return None
