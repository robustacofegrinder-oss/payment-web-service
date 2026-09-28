from flask import Flask, jsonify
import sys
import payment_config as config
from payment_orders import create_order, verify_order_payment, get_orders, attach_license

sys.path.insert(0, "licensing/admin")
from issue_customer import issue_customer

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({"service": "payment-api", "status": "ok"})

@app.post("/create-order")
def create_payment_order():
    order = create_order(config.LICENSE_PRICE_USDT)
    return jsonify({
        "order_id": order["order_id"],
        "amount_usdt": order["amount_usdt"],
        "currency": order["currency"],
        "network": order["network"],
        "status": order["status"]
    })

@app.get("/check-payment/<order_id>")
def check_payment(order_id):
    orders = get_orders()
    target = next((o for o in orders if o.get("order_id") == order_id), None)

    if not target:
        return jsonify({"error": "order_not_found"}), 404

    order = verify_order_payment(order_id)

    if not order:
        return jsonify({
            "order_id": order_id,
            "status": "PENDING"
        })

    if order.get("status") != "PAID":
        return jsonify({"order_id": order_id, "status": "PENDING"})

    if order.get("license_key"):
        return jsonify({
            "order_id": order_id,
            "status": "PAID",
            "license_key": order["license_key"]
        })

    record = issue_customer(order_id)
    updated = attach_license(order_id, record["key"])

    return jsonify({
        "order_id": order_id,
        "status": "PAID",
        "license_key": updated["license_key"]
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081)
