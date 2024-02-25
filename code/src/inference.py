from typing import Dict, Tuple
from pycoral.adapters.common import input_size
from pycoral.adapters import common
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
import collections

import cv2
import numpy as np

Object = collections.namedtuple("Object", ["id", "score", "bbox"])


class BBox(collections.namedtuple("BBox", ["xmin", "ymin", "xmax", "ymax"])):
    """Bounding box.
    Represents a rectangle which sides are either vertical or horizontal, parallel
    to the x or y axis.
    """

    __slots__ = ()


def _get_output(interpreter, score_threshold, top_k):
    """Returns list of detected objects."""
    pass


# class Config(TypedDict):


class Inference:
    interpreter = None
    labels: Dict[int, str]
    size: Tuple[int, int] = None

    def __init__(self):
        self.interpreter = make_interpreter(
            "./models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite"
        )
        self.interpreter.allocate_tensors()

        self.labels = read_label_file("./models/coco_labels.txt")
        self.size = common.input_size(self.interpreter)

    def infer(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        resized_image = cv2.resize(rgb_image, self.size)
        common.set_input(self.interpreter, resized_image)
        self.interpreter.invoke()

        boxes = common.output_tensor(self.interpreter, 0)
        category_ids = common.output_tensor(self.interpreter, 1)
        scores = common.output_tensor(self.interpreter, 2)

        print(boxes[0][0])

        print(
            "score={:.2f}: {}".format(
                scores[0][0], self.labels[int(category_ids[0][0])]
            )
        )
