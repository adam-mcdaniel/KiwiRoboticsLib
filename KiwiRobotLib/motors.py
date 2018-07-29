import wpilib
import ctre
import time


class TalonMotor(ctre.wpi_talonsrx.WPI_TalonSRX):
    """
    This class is used to interface with the TalonSRX
    motor controller.
    """
    def __init__(self, CAN_Id):
        super().__init__(CAN_Id)

    def getSpeed(self):
        """
        This function returns the speed in inches per second.
        """
        return (self.getPulseWidthVelocity() / 4096) * 6 * 3.14159

    def getPosition(self):
        """
        This function returns the distance travelled in inches.
        """
        return (self.getQuadraturePosition() / 4096) * 6 * 3.14159

    def getRawPosition(self):
        """
        This function returns the distance travelled using: 4096 units = 1 rotation
        """
        return self.getQuadraturePosition()

    def resetPosition(self):
        """
        This function resets the encoder position to 0
        """
        self.setQuadraturePosition(0, 0)

    def invert(self):
        """
        This function inverts the motor.
        """
        self.setInverted(True)
        