from typing import TypedDict
from src import (
    params,
    vehicle as vehicle_module,
    camera as camera_module,
    object_detection as object_detection_module,
    distance_sensor as distance_sensor_module,
    led as led_module,
    switch as switch_module,
)
from src.brains import ModuleTypes as BrainModuleTypes, Types as BrainTypes
import json


class Config(TypedDict):
    brains: BrainModuleTypes
    camera: camera_module.Config
    object_detection: object_detection_module.ObjectDetection
    distance_sensors: list[distance_sensor_module.Config]
    leds: list[led_module.LED]
    switches: list[switch_module.Switch]
    vehicle: vehicle_module.Config


# read from config.json
config: Config = json.loads(params.CONFIG_PATH.read_text())

# Load Camera
camera_config = config["camera"]
camera = camera_module.Camera(camera_config)

object_detection_config = config["object_detection"]
object_detection = object_detection_module.ObjectDetection(object_detection_config)

# Load Distance Sensors
distance_sensors_config = config["distance_sensors"]
distance_sensors: list[distance_sensor_module.DistanceSensor] = []
for d in distance_sensors_config:
    distance_sensors.append(distance_sensor_module.DistanceSensor(d))

# Load LEDs
leds_config = config["leds"]
leds: list[led_module.LED] = []
for d in leds_config:
    leds.append(led_module.LED(d))

# Load Switches
switches_config = config["switches"]
switches: list[switch_module.Switch] = []
for d in switches_config:
    switches.append(switch_module.Switch(d))

# Load Vehicle
vehicle_config = config["vehicle"]
vehicle = vehicle_module.Vehicle(vehicle_config)

# Load Brain
brain_type = "autonomous"

# merge the base brain config with the brain-specific config, giving priority to the brain-specific config
brain_config = {**config["brains"]["base"], **config["brains"][brain_type]}
brain_module = BrainTypes[brain_type]

# initialize a brain instance from whichever brain module you loaded
brain = brain_module.Brain(
    brain_config, camera, object_detection, distance_sensors, leds, switches, vehicle
)

from flask import Flask, Response, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS  # Import CORS
from werkzeug.utils import secure_filename
import os
import datetime
import threading
import cv2

# sample command line post request
# curl -X POST -F "picture=@/path/to/picture.jpg" -F "number_of_items=5" -F "coordinates=40.45,67.89" http://127.0.0.1:5000/api/pictureitem
# to run app, run python3 server.py

app = Flask(__name__, static_url_path='', static_folder="website")
CORS(app)  # Enable CORS for the entire app
api = Api(app)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory storage for demonstration
data_storage = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class PictureItem(Resource):
    def get(self):
        # Return the stored data
        return jsonify(data_storage)

    def post(self):
        if 'picture' not in request.files:
            return {'message': 'No picture part'}, 400
        file = request.files['picture']
        if file.filename == '':
            return {'message': 'No selected file'}, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Save data
            item_data = {
                'timestamp': datetime.datetime.now().isoformat(),
                'number_of_items': request.form.get('number_of_items', type=int),
                'coordinates': request.form.get('coordinates'),
                'picture_url': file_path
            }
            data_storage.append(item_data)

            return item_data, 201

class StreamVideo(Resource):
    def get(self):
        return Response(create_response(), mimetype="multipart/x-mixed-replace; boundary=frame")

def create_response():
    while True:
        if not brain.object_detection.image.any():
            continue

        ret, frame = cv2.imencode(".jpg", brain.object_detection.image)
        if not ret:
            continue

        yield (
            b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + bytearray(frame) + b"\r\n"
        )

api.add_resource(StreamVideo, '/stream')
api.add_resource(PictureItem, '/api/pictureitem')

threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)).start()


# Tell the brain to drive the vehicle
try:
    brain.run()
except KeyboardInterrupt:
    vehicle.stop()


