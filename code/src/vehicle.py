from typing import TypedDict
from . import motor

# The two motors run at different speeds with the same PWM signal, so we throttle the left motor manually.
LEFT_MOTOR_SCALE = 0.77877


class MotorsConfig(TypedDict):
    left: motor.Config
    right: motor.Config


class Config(TypedDict):
    motors: MotorsConfig


class Vehicle:

    left_motor: motor.Motor
    right_motor: motor.Motor

    def __init__(self, config: Config):

        self.left_motor = motor.Motor(config['motors']['left'])
        self.right_motor = motor.Motor(config['motors']['right'])

    def stop(self) -> None:
        """stop both motors"""
        self.left_motor.stop()
        self.right_motor.stop()

    def drive_forward(self, speed: float = 1.0) -> None:
        """turn both motors forward at a given speed"""
        self.left_motor.forward(speed * LEFT_MOTOR_SCALE)
        self.right_motor.forward(speed)

    def drive_backward(self, speed: float = 1.0) -> None:
        """turn both motors backward at a given speed"""
        self.left_motor.backward(speed * LEFT_MOTOR_SCALE)
        self.right_motor.backward(speed)

    def pivot_left(self, speed: float = 1.0) -> None:
        """at the same speed, drive the left motor backward, and the right motor forward"""
        self.left_motor.backward(speed)
        self.right_motor.forward(speed)

    def pivot_right(self, speed: float = 1.0) -> None:
        """at the same speed, drive the left motor forward, and the right motor backward"""
        self.left_motor.forward(speed)
        self.right_motor.backward(speed)

    def onlyright(self, speed: float = 1.0) -> None:
        self.left_motor.forward(speed)

    def onlyleft(self, speed: float = 1.0) -> None:
        self.right_motor.forward(speed)

    def onlyrightb(self, speed: float = 1.0) -> None:
        self.left_motor.backward(speed)

    def onlyleftb(self, speed: float = 1.0) -> None:
        self.right_motor.backward(speed)

    def drive(self, left_speed: float, left_direction: bool, right_speed: float, right_direction: bool) -> None:
        """Control each motor's speed and direction independently"""

        self.left_motor.drive(left_speed, left_direction)
        self.right_motor.drive(right_speed, right_direction)
