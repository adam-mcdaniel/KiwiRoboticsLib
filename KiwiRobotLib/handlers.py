import wpilib
import ctre
import time
from .motors import *
from .pnuematics import *
from collections import deque

class Handler(deque):
    """
    This is the baseclass for all of the different
    handlers, such as the Solenoid handler.

    This class is meant to allow objects of the same or
    similar types to be grouped together and to be controlled
    as a whole.
    """
    def __init__(self, *args):
        for item in args:
            self.append(item)

    def __call__(self, method, *args):
        """
        This allows the handler to be called like a function
        to run a function on all of the handlers children.

        For example:
            '''
            h = Handler(TalonMotor(1),
                        TalonMotor(2))
            h(TalonMotor.set, 1)
            '''
        This code will set the Handler's talon motors to
        100%.
        
        This is identical to:
            '''
            h = Handler(TalonMotor(1),
                        TalonMotor(2))
            h.handle(TalonMotor.set, 1)
            '''
        """
        list(map(lambda a: method(a, *args), self))

    def handle(self, method, *args):
        """
        This function is identical to the __call__
        function of this class.

        It allows the handler to call a function on all
        of the handlers children.
        
        Here's an example:
            '''
            h = Handler(TalonMotor(1),
                        TalonMotor(2))
            h.handle(TalonMotor.set, 1)
            '''
        This code will set the Handler's talon motors to
        100%.
        """
        list(map(lambda a: method(a, *args), self))


def set(motor, speed):
    """
    This function is used by the MotorHandler class
    to set the speed of a motor.
    """
    motor.set(speed)

def invert(motor):
    """
    This function is used by the MotorHandler class
    to invert a motor.
    """
    motor.Invert()


class MotorHandler(wpilib.SpeedControllerGroup):
    """
    This handler is used to group motors together
    and to control them as a whole.
    """
    def __init__(self, *args):
        for motor in args:
            if not type(motor) in [TalonMotor]:
                raise Exception("You need to use the motor classes in KiwiRobotLib.motors.\nInstead you used: {}".format(type(motor)))

        self.handler = Handler(*args)
        self.args = args
        if len(self.handler) > 0:
            super().__init__(*args)

    def __call__(self, method, *args):
        """
        See Handler.__call__
        """
        list(map(lambda a: method(a, *args), self.handler))

    def handle(self, method, *args):
        """
        See Handler.handle
        """
        list(map(lambda a: method(a, *args), self.handler))

    def append(self, a):
        """
        This adds a motor object to the handler.
        """
        self.handler.append(a)
        if len(self.handler) == 1:
            super().__init__(*self.handler)

    def __len__(self):
        return len(self.handler)

    def __getitem__(self, n):
        return self.handler[n]

    def __iter__(self):
        return self.handler.__iter__()

    def invert(self):
        """
        This inverts all of the motors in the handler.
        """
        self.handle(invert)

    def set(self, s):
        """
        This sets the speed of all the motors
        in the handler to a given percent.
        """
        self.handle(set, s)


def push(s):
    """
    This function is used by the SolenoidHandler
    class to "push" a pnuematic press using a solenoid.
    """
    s.push()

def pull(s):
    """
    This function is used by the SolenoidHandler
    class to "pull" a pnuematic press using a solenoid.
    """
    s.pull()


class SolenoidHandler(Handler):
    """
    This handler is used to group motors together
    and to control them as a whole.
    """
    def __init__(self, *args, pcm=20):
        SetIdPCM(pcm)
        for solenoid in args:
            if not type(solenoid) in [Solenoid]:
                raise Exception("You need to use the motor classes in KiwiRobotLib.motors.\nInstead you used: {}".format(type(solenoid)))
        super().__init__(*args)

    def push(self):
        """
        This "pushes" with all of the solenoids in the group.
        """
        super().handle(push)

    def pull(self):
        """
        This "pulls" with all of the solenoids in the group.
        """
        super().handle(pull)
