import wpilib
import time


class Gyro(wpilib.adxrs450_gyro.ADXRS450_Gyro):
    """
    This class is used to interface with the ADXRS450 Gyro.
    It isn't important, it only adds the option of a scale factor.
    """
    def __init__(self, scale_factor=1):
        self.scale_factor = scale_factor
        super().__init__()

    def getAngle(self):
        return super().getAngle() * self.scale_factor


class UltraSonicSensor():
    """
    This class is used to interface with the
    analog ultrasonic sensors from the MB series
    (like the MB1010, MB1200, etc.)
    """
    def __init__(self, channel):
        """
        The class takes one parameter, the analog-input
        channel number of the ultrasonic sensor.
        """
        self.analog_input = wpilib.analoginput.AnalogInput(channel)
        self.inches_away = 83.99972 * self.analog_input.getAverageVoltage()
        self.cycle_limit = 4

    def AvgInchesAway(self):
        """
        This function takes a rolling average of the distance
        measured by the sensor. The units of the returned value are inches.
        """
        self.inches_away *= (self.cycle_limit - 1) / self.cycle_limit
        self.inches_away += (83.99972 * self.analog_input.getAverageVoltage()) / self.cycle_limit
        return self.inches_away

    def InchesAway(self):
        """
        This function takes the current distance
        measured by the sensor. The units of the returned value are inches.
        """
        return 83.99972 * self.analog_input.getAverageVoltage()
