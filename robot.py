import time
import wpilib
from KiwiRobotLib.motors import *
from KiwiRobotLib.handlers import *
from KiwiRobotLib.subsystem import *


class HiroChassis(BasicChassis):
    def update(self, joystick):
        self.arcadeDrive(joystick.getRawAxis(1)*0.8,
                         joystick.getRawAxis(2)*0.8)


class HiroElevator(BasicElevator):
    def update(self, joystick):
        if joystick.getRawButton(1):
            super().update("Up")
        elif joystick.getRawButton(2):
            super().update("Down")
        else:
            super().update("None")

# class HiroClaw(Subsystem):
#     def __init__(self):
#         self.solenoids = SolenoidHandler(Solenoid(0, 1),
#                                          Solenoid(2, 3),
#                                          pcm=20)
#         self.left_motors = MotorHandler(TalonMotor(1),
#                                         TalonMotor(2))
#         self.right_motors = MotorHandler(TalonMotor(1),
#                                         TalonMotor(2))
#         self.thread(self.background_proc)

#     def update(self, joystick):
#         print("updating...")

#     def background_proc(self):
#         while True:
#             print("waiting...")
#             time.sleep(1)


class Hiro(wpilib.IterativeRobot):
    def robotInit(self):
        self.joystick = wpilib.Joystick(0)

        self.elevator = HiroElevator(TalonMotor(4))

        self.chassis = HiroChassis(TalonMotor(0),
                                   TalonMotor(1),
                                   TalonMotor(2),
                                   TalonMotor(3))

        # self.claw = HiroClaw()

    def teleopPeriodic(self):
        # self.claw.update(self.joystick)
        self.elevator.update(self.joystick)
        self.chassis.update(self.joystick)


if __name__ == "__main__":
    wpilib.run(Hiro)
