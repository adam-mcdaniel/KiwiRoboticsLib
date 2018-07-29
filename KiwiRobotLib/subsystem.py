import wpilib
from .handlers import *
from wpilib import drive
from functools import reduce
import threading


class Subsystem:
    """
    The Subsystem class is the baseclass for all subsystems in the framework.

    An example usage of this baseclass would be:
        '''
        class Claw(Subsystem):
            def __init__(self):
                self.solenoids = SolenoidHandler(left_claw_solenoid,
                                                right_claw_solenoid,
                                                pcm=20)

                self.left_motors = MotorHandler(front_left_claw_motor,
                                                back_left_claw_motor)
                self.right_motors = MotorHandler(front_right_claw_motor,
                                                back_right_claw_motor)
                
                self.thread(self.background_proc)

            def update(self, joystick):
                pass

            def background_proc(self):
                while True:
                    print("waiting...")
                    time.sleep(1)
        '''
    """
    def __init__(self):
        pass

    def update(self, *args):
        
        """
        This function is intended to be overwritten.

        Use this function during teleop to pass
        joystick data or other data to the subsystem.
        """
        pass

    def thread(self, method, *args):
        """
        This function allows a system to start a process that runs
        in the background.

        This could be used for several things, such as monitoring encoder
        values and shifting gears accordingly.

        :param method: The function to run in the background
        :param args: The arguments to be passed to the function ran in the background
        """
        threading.Thread(target=method, args=tuple(args)).start()


class BasicChassis(drive.DifferentialDrive, Subsystem):
    """
    This class is a quick and easy way to make a chassis, although it
    should be modified for gear shifting, etc.

    It takes 2, 4, or 6 motor objects.
    
    The first half of the motors are considered the "left" motors.
    The second half of the motors are considered the "right" motors.
    """
    def __init__(self, *args):
        if len(args) == 2:
            super().__init__(args[0], args[1])
        elif len(args) == 4:
            self.left = MotorHandler(*args[:2])
            self.right = MotorHandler(*args[2:4])
            super().__init__(self.left, self.right)
        elif len(args) == 6:
            self.left = MotorHandler(*args[:3])
            self.right = MotorHandler(*args[3:6])
            super().__init__(self.left, self.right)
        else:
            raise Exception("Unable to create Chassis instance.\nThe number of motors used to create an instance of the Chassis is not valid.")
        self.setSafetyEnabled(False)

    def update(self, joystick, buttons=None):
        """
        This function should be overwritten, it is only here because
        this class is intended to be useful without writing a bunch of
        code first.
        """
        self.arcadeDrive(joystick.getRawAxis(1),
                         joystick.getRawAxis(2))


class BasicElevator(Subsystem):
    """
    This class is a quick and easy way to make an elevator, but
    it really should be modified for use in a competition.

    It takes any number of motor objects,
    an upward speed between -1 and 1,
    and a downard speed between -1 and 1.
    """
    def __init__(self, *args, up_speed=0, down_speed=0):
        self.up_speed = up_speed
        self.down_speed = down_speed
        self.current_limit = 38
        self.motors = args

    def update(self, direction="None"):
        """
        This function should be overwritten if
        necessary, but in most cases it shouldnt be.

        This function should just be used through "super()",
        and called to move the elevator up and down.
        """
        if direction == "Up":
            if reduce(lambda a, m: abs(m.getOutputCurrent()) if abs(m.getOutputCurrent()) > a else a, self.motors, 0) > self.current_limit:
                pass
            else:
                list(map(lambda m: m.set(self.up_speed),
                         self.motors))

        elif direction == "Down":
            if reduce(lambda a, m: abs(m.getOutputCurrent()) if abs(m.getOutputCurrent()) > a else a, self.motors, 0) > self.current_limit:
                pass
            else:
                list(map(lambda m: m.set(self.down_speed),
                        self.motors))

        else:
            pass

    def setCurrentLimit(self, current):
        """
        This function sets the current limit so that
        the elevator stops moving when the current
        reaches that limit.
        """
        self.current_limit = current
        