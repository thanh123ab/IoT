import base64
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time
import torch
from flask import Flask, render_template, Response, jsonify
from datetime import datetime
import mysql.connector
from sympy import false
from ultralytics import YOLO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔧 Kết nối MySQL
conn = mysql.connector.connect(
    host="quanlybaido.duckdns.org",
    port="3306",
    user="admin",
    password="admin",
    database="demgt"
)
cursor = conn.cursor()

# 🔧 Cấu hình MQTT
MQTT_BROKER = "192.168.1.13"
MQTT_PORT = 1883
MQTT_TOPIC = "img"

# Load mô hình YOLOv8 nhận diện phương tiện
model = YOLO(r'C:\Users\Asus\PycharmProjects\IotT\train3\weights\best.pt')
model.eval()

# Biến toàn cục lưu ảnh từ MQTT
image_data = {}
total_parts = None
latest_image = None


def fix_base64_padding(base64_string):
    missing_padding = len(base64_string) % 4
    if missing_padding:
        base64_string += "=" * (4 - missing_padding)
    return base64_string


def detect_vehicle(image):
    global latest_image
    results = model(image)  # Nhận diện phương tiện
    image_cv = results[0].plot()

    vehicle_detected = any(cls in [0, 1, 2, 3] for _, _, _, _, _, cls in results[0].boxes.data.tolist())

    _, buffer = cv2.imencode('.jpg', image_cv)
    latest_image = buffer.tobytes()

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 📌 Lưu dữ liệu vào MySQL
    try:
        cursor.execute("INSERT INTO dem_xe (data_xe, times) VALUES (%s, %s)", (int(vehicle_detected), current_time))
        conn.commit()
        print(f"🚗 Đã lưu vào MySQL: {int(vehicle_detected)} - {current_time}")
    except Exception as e:
        print(f"❌ Lỗi khi lưu vào MySQL: {e}")

    return vehicle_detected


def on_message(client, userdata, msg):
    global image_data, latest_image, total_parts

    message = msg.payload.decode()

    if message == "end":
        if total_parts is not None and len(image_data) == total_parts:
            try:
                full_image_data = "".join(image_data[i] for i in sorted(image_data.keys()))
                full_image_data = fix_base64_padding(full_image_data)

                image_bytes = base64.b64decode(full_image_data)
                np_arr = np.frombuffer(image_bytes, np.uint8)
                current_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                if current_image is not None:
                    print("🚗 Ảnh nhận thành công! Chạy nhận diện phương tiện...")
                    detect_vehicle(current_image)

            except Exception as e:
                print(f"❌ Lỗi khi xử lý ảnh: {e}")

        image_data.clear()
        total_parts = None
    else:
        try:
            index, part = message.split(":", 1)
            part_index, total = map(int, index.split("/"))
            total_parts = total
            image_data[part_index] = part
        except Exception as e:
            print(f"❌ Lỗi khi xử lý phần ảnh: {e}")


client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)
client.loop_start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_chart_data')
def get_chart_data():
    cursor.execute("SELECT times, data_xe FROM dem_xe ORDER BY times DESC LIMIT 50")
    data = cursor.fetchall()

    timestamps = [row[0].strftime("%Y-%m-%d %H:%M:%S") for row in data]
    vehicle_status = [row[1] for row in data]

    return jsonify({"timestamps": timestamps, "vehicle_status": vehicle_status})


def generate():
    global latest_image
    while True:
        if latest_image:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + latest_image + b'\r\n')
        time.sleep(0.1)


@app.route('/esp_feed')
def esp_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
