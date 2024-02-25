from src import camera as camera_module
from src import object_detection as object_detection_module
import time

if __name__ == "__main__":
    total_seconds = 60

    camera = camera_module.Camera({"show_preview": False})
    object_detection = object_detection_module.ObjectDetection(
        {"model_path": "./model_full_integer_quant_edgetpu.tflite"}
    )
    start_time = time.time()

    while time.time() - start_time < total_seconds:
        camera.capture()
        results = object_detection.predict(camera.image_array)
        results[0].show()

        time.sleep(1)
