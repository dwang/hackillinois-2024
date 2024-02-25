from ultralytics import YOLO
from ultralytics.engine.results import Results
from torch.nn import Module
from typing import TypedDict
import cv2


class Config(TypedDict):
    model_path: str
    image_size: list[int]

class ObjectDetection:
    model: Module
    image_size: list[int]
    prediction: Results

    def __init__(self, config: Config):
        self.model = YOLO(config["model_path"])
        self.image_size = config["image_size"]

    def predict(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.model.predict(rgb_image, imgsz=self.image_size)
        self.prediction = results[0]

