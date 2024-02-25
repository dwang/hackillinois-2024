from . import base
import time


class Config(base.Config):
    pass


class Brain(base.Brain):
    """The autonomous Brain object, drives the vehicle autonomously based on information gathered by the sensors"""

    def __init__(self, config: Config, *arg):
        super().__init__(config, *arg)

    picwidth = 640
    timesright = 0
    timesleft = 0
    movetime = 0
    centered = False
    currnum = 1

    def turn7p5right(self):
        print("turning 7.5 degrees right")
        # self.vehicle.onlyrightb(0.3)
        self.vehicle.pivot_right(0.8)
        # time.sleep(0.02)
        # self.vehicle.onlyright(0.5)
        time.sleep(0.1)
        self.vehicle.stop()

    def turn7p5left(self):
        print("turning 7.5 degrees left")
        self.vehicle.pivot_left(0.8)
        # self.vehicle.onlyleftb(0.3)
        # time.sleep(0.02)
        # self.vehicle.onlyleft(0.8)
        time.sleep(0.12)
        self.vehicle.stop()

    def movetowards(self):
        print("GOOOO")
        print("times right " + str(self.timesright))
        print("times left " + str(self.timesleft))
        while self.distance_sensors[1].distance > 0.10:
            self.vehicle.drive_forward(0.6)
            time.sleep(0.1)
            self.vehicle.stop()
            time.sleep(0.1)
            self.movetime += 1
        while self.movetime > 0:
            self.vehicle.drive_backward(0.6)
            time.sleep(0.1)
            self.vehicle.stop()
            time.sleep(0.1)
            self.movetime -= 1
        while (self.timesright) > 0:
            self.turn7p5left()
            self.timesright -= 1
        while (self.timesleft) > 0:
            self.turn7p5right()
            self.timesleft -= 1
        self.centered = False
        return True

    def centertrash(self, x):
        print("running centering thing")
        if (x > self.picwidth / 2 - 45 and x < self.picwidth / 2 + 45) or (
            self.timesright != 0 and self.timesleft != 0
        ):
            if self.timesright != 0 and self.timesleft != 0:
                self.timesright -= 1
                self.timesleft -= 1

            self.centered = True
        if x < self.picwidth / 2 - 40:
            self.turn7p5left()
            self.timesleft += 1
        if x > self.picwidth / 2 + 40:

            self.turn7p5right()
            self.timesright += 1

    def logic(self):
        """If anything is detected by the distance_sensors, stop the car"""
        if (
            self.distance_sensors[0].distance < 0.1
            and self.distance_sensors[1].distance < 0.1
        ):
            print("WALLL")
            self.running = False

        if self.centered:
            if self.movetowards():
                print("done collect")

        with self.lock:
            if self.object_detection.prediction:
                x, _, _, _ = self.object_detection.prediction.boxes.xywh.tolist()[0]
                self.centertrash(x)
            else:
                if self.currnum % 31 == 0:
                    print("trying to mvoe")
                    self.vehicle.drive_forward()
                    time.sleep(0.5)
                    self.vehicle.stop()
                else:
                    self.vehicle.pivot_right(0.8)
                    time.sleep(0.1)
                    self.vehicle.stop()
                self.currnum += 1
        time.sleep(1)
