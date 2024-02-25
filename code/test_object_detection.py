from src import camera as camera_module
from src import object_detection as object_detection_module
import time
import cv2

if __name__ == "__main__":
    total_seconds = 60

    camera = camera_module.Camera({"show_preview": False})
    object_detection = object_detection_module.ObjectDetection(
        {"model_path": "./model_full_integer_quant_edgetpu.tflite", "image_size": [352, 352]}
    )
    start_time = time.time()

    while time.time() - start_time < total_seconds:
        camera.capture()
        object_detection.predict(camera.image_array)
        if object_detection.prediction:
            object_detection.prediction.save("result.jpg")
        else:
            cv2.imwrite("result.jpg", cv2.cvtColor(camera.image_array, cv2.COLOR_BGR2RGB))
        time.sleep(2)
