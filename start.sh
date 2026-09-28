python3 payment_api.py &
exec gunicorn --bind 0.0.0.0:$PORT payment_web_ui:app
