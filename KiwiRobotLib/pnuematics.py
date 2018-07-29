import wpilib

compressor = wpilib.Compressor()

pcm = 20


def SetIdPCM(n):
    """
    This function is used by the solenoid handlers.
    It sets the CAN ID of the PCM for the rest of
    the robot code.

    The default ID is 20.
    
    This does not mean this changes the CAN ID of
    the PCM!!!
    That has to be changed with the roborio web
    configuration utility!!!
    """
    global pcm
    pcm = n


class Solenoid(wpilib.DoubleSolenoid):
    """
    This class is used for representing solenoids
    on the robot.
    """
    def __init__(self, push=0, pull=1):
        super().__init__(pcm, push, pull)

    def push(self):
        """
        If you don't know what push means, you are dumb.
        """
        super().set(wpilib.DoubleSolenoid.Value.kForward)

    def pull(self):
        """
        If you don't know what pull means, you are dumb.
        """
        super().set(wpilib.DoubleSolenoid.Value.kReverse)
