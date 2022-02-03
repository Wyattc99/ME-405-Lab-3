"""!
@file positioncontrol.py
Control Motor's position
@author Jacob Wong
@author Wyatt Conner
@author Jameson Spitz
@date   27-Feb-2
@copyright by Jameson Spitz all rights reserved
"""
# from motordriver import MotorDriver
# from encoderdriver import EncoderDriver

class PositionControlTask():
    """!
    This class contains the methods to create a feed back control system using a 
    motor and encoder. the motor is acting as the the plant of the system and the 
    encoder is the sensor of the system. This class
    has the methods to actually complete this by checking the position and updating the
    error of the system and calculating the new data of the sy
    """
    
    def __init__(self, Motor, Encoder):
        """!
        This method initializes the position control object so we can create multiple
        objects for various encoder motor systems. This also initalizes our object variables
        """
        ## This variable passes the motor object into the position control object
        self.Motor = Motor
        ## This variable passes the encoder object into the position control object
        self.Encoder = Encoder
        ## This initilizing our controllers gain as zero as it will be referenced for other methods
        self.gain = 0
        ## This initilizes the desired position we want the motor to achieve
        self.setpoint = 0
        ## This initilizes the error variable to represent the difference of position to our actual position
        self.error = 0
    
    def set_point(self):
        """!
        This method is used to set the desired position of the encoder for the motor
        to achieve, this is the input to our control system. It is set up to take this value
        in units of encoder ticks. Each rotation is 16,000 ticks. 
        """
        try:
            self.setpoint = float(input('Enter desired position value in ticks \n'))
            while self.setpoint == 0:
                self.setpoint = float(input('The set point cannot be zero enter a valid value \n'))
        except:
            print('Please enter a valid number for the set point')
            
    def set_gain(self):
        """!
        This method is used to set the gain of the porportional controller for the
        position controller. This gain is multiplied by the error of the posisiton
        to calculate the duty cycle to send to the motor. 
        """
        try:
            self.gain = float(input('Enter desired porportional gain value \n'))
        except:
            print('Please enter a valid number for the gain')
    
    def position_control(self):
        """!
        This method used in an external loop to control the motor and encoder
        pair for the desired location. This method updates the encoder position,
        and calculates the error of system with the difference of the current
        position to the desired position, this is multiplied by the gain to calculate
        the duty cycle of the motor each iteration. 
        """
        # Update the encoder position
        self.Encoder.update_delta()
        
        ## This variable is used to store the ticks value of the encoder
        self.position = self.Encoder.get_position()
        
        self.error = (-self.position + self.setpoint)/self.setpoint
        
        if self.error > 0:
            ## Duty is represents the duty cycle being sent to the motor object
            self.duty = self.gain*self.error + 15
        elif self.error < 0:
            self.duty = self.gain*self.error - 15
        else:
            self.duty = 0
        
        self.Motor.set_duty_cycle(self.duty)
    
    