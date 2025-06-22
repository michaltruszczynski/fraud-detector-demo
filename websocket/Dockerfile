FROM python:3.10

WORKDIR /app
COPY . .
RUN pip install flask flask_socketio

CMD ["python", "websocket_server.py"]