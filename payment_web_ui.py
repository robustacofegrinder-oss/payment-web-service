from flask import Flask, jsonify, render_template, send_file
import urllib.request, json
app=Flask(__name__)
API="http://127.0.0.1:8081"
WALLET="TJMFEyA6QbbkHtNH52NsCPcPVA9AZpBWoq"
@app.get("/")
def home():
    return send_file("landing_preview.html")

@app.get("/payment")
def payment():
    return render_template("payment_page.html")
@app.post("/create-order")
def create():
    r=urllib.request.urlopen(urllib.request.Request(API+"/create-order",method="POST"))
    return jsonify(json.loads(r.read()))
@app.get("/check-payment/<order_id>")
def check_web(order_id):
    r=urllib.request.urlopen(API+"/check-payment/"+order_id)
    return jsonify(json.loads(r.read()))
if __name__ == "__main__": app.run(host="0.0.0.0",port=8080)
