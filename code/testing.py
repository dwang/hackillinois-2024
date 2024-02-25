from src import vehicle as vehicle_module
from src import distance_sensor as distance_sensor_module
import time

if __name__ == '__main__':
    total_seconds = 60
    sample_hz = 2

    distance_sensor1 = distance_sensor_module.DistanceSensor({
        "pins": {
            "echo": 23,
            "trigger": 24
        }
    })

    distance_sensor2 = distance_sensor_module.DistanceSensor({
        "pins": {
            "echo": 17,
            "trigger": 27
        }
    })

    vehicle = vehicle_module.Vehicle(
        {
            "motors": {
                "left": {
                    "pins": {
                        "speed": 13,
                        "control1": 5,
                        "control2": 6
                    }
                },
                "right": {
                    "pins": {
                        "speed": 12,
                        "control1": 7,
                        "control2": 8
                    }
                }
            }
        }
    )
    


    timesright = 0
    timesleft = 0

    # print('Forward')
    # vehicle.drive_forward(1)
    # time.sleep(3)
    def centertrash(maxx,minx):
        if ((maxx - minx)/2 > -20 and (maxx - minx)/2 < 20) or (timesright != 0 and timesleft != 0):
            timesright -= 1
            timesleft -= 1
            return True
        if (maxx - minx)/2 < -20:
            turn7p5left()
            timesleft += 1
        if (maxx - minx)/2 > 20:
            turn7p5right()
            timesright += 1
        return False
    
    movetime = 0


    def movetowards():
        while(distance_sensor1.distance < 5 and distance_sensor2.distance < 5):
            vehicle.drive_forward(0.1)
            time.sleep(0.1)
            movetime += 1
        if timesright != 0:
            for x in range(timesright):
                turn7p5left()
                turn7p5left()
        else:
            for x in range(timesleft):
                turn7p5right()
                turn7p5right()
        while movetime != 0:
            vehicle.drive_forward(0.1)
            movetime -= 1
        while(timesright) != 0:
            turn7p5right()
            timesright -= 1
        while(timesleft) != 0:
            turn7p5right()
            timesleft -= 1
        vehicle.drive_forward(1)
        time.sleep(1)
        vehicle.stop()

    def turn7p5right():
        vehicle.onlyrightb(0.3)
        time.sleep(0.02)
        vehicle.onlyright(0.351)
        time.sleep(0.2)
        vehicle.stop()
    def turn7p5left():
        vehicle.onlyleftb(0.3)
        time.sleep(0.02)
        vehicle.onlyleft(0.5)
        time.sleep(0.2)
        vehicle.stop()

    def turn90right():
        vehicle.onlyrightb(0.9)
        time.sleep(0.02)
        vehicle.onlyright(0.8)
        time.sleep(0.66)
        vehicle.stop()
    
    def turn90left():
        vehicle.onlyleftb(0.9)
        time.sleep(0.01)
        vehicle.onlyleft(0.9)
        time.sleep(0.8)
        vehicle.stop()
    
    for x in range(48):

