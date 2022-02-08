"""!
@file motordriver.py
This file configures Nucleo pins, timers, and channels for so that it can send voltage to a motor.
Can send a PWM duty cycle to the motor to control how fast the motor spins. Uses a L6206 motor shield to control motor direction.
@author Jacob Wong
@author Wyatt Conner
@author Jameson Spitz
@date   26-Jan-22
@copyright by Jameson Spitz all rights reserved
"""

import pyb
import time

class MotorDriver():
    
    """!
    Initializes motor pins allowing for the motor to rotate in both directions. Can initialize multiple motors
    because each motor object will have its own pins, timers, and channels.
    """
    
# Motor 1 (tim3)
# p1 = pyb.Pin.board.PB4
# p2 = pyb.Pin.board.PB5
# en = pyb.Pin.board.PA10
# Motor 2 (tim5)
# p1 = pyb.Pin.board.PA0
# p2 = pyb.Pin.board.PA1
# en = pyb.Pin.board.PC1
    
    def __init__(self, pin1, pin2, pin_enable, timer):
        
        """!
        Initialize pins, timers and chanels.
        @param pin1 First pin connected to motor.
        @param pin2 Second pin connected to motor.
        @param pin_enable Enables motor to have a duty cycle set.
        @param timer Timer number specified from datasheet for pins used.
        """
        
        ## pinIN1A Set as output pin and connected to Motor 
        self.pinIN1A = pyb.Pin(pin1, pyb.Pin.OUT_PP)
        
        ## pinIN2A Set as output pin and connected to Motor
        self.pinIN2A = pyb.Pin(pin2, pyb.Pin.OUT_PP)

        ## pinENOCDA Set as PULL_UP pin to enable motor
        self.pinENOCDA = pyb.Pin(pin_enable, pyb.Pin.IN, pull = pyb.Pin.PULL_UP)

        ## tim3 is the timer for motor control
        self.tim3 = pyb.Timer(timer, freq = 20000)

        ## t3ch1 Sets input pin1 on timer 3 channel 1 to control PWM
        self.t3ch1 = self.tim3.channel(1, pyb.Timer.PWM, pin = self.pinIN1A)
        
        ## t3ch2 Sets input pin1 on timer 3 channel 2 to control PWM
        self.t3ch2 = self.tim3.channel(2, pyb.Timer.PWM, pin = self.pinIN2A)

    def set_duty_cycle(self, duty):
        
        """!
        Accepts a duty cycle percentage and sets it as a pwm to nucleo channels.
        Sets the duty to move motor backwards or forwards.
        @param duty is the PWM a user wants to run the motor at.
        """
        # Accounting for positive saturation
        if (duty > 100):
            duty = 100
        
        # Accounting for negative saturation
        elif (duty < -100):
            duty = -100
            
        # Make motor rotate forwards if positive duty cycle
        if (duty > 0):
                self.t3ch1.pulse_width_percent(0)
                self.t3ch2.pulse_width_percent(abs(duty))
                
        # Make motor rotate backwards if negative duty cycle       
        elif (duty <= 0):
                self.t3ch1.pulse_width_percent(abs(duty))
                self.t3ch2.pulse_width_percent(0)
        #print(duty)
        
    def enable(self):
        """!
        This method is called to enable the pin on the board to allow current
        flow to the motor to enable motion of the motor. 
        """
        self.pinENOCDA.high()
          
if __name__ == "__main__":
    
    ## motor1 Motor object 1.
    motor1 = MotorDriver(pyb.Pin.board.PB4, pyb.Pin.board.PB5, pyb.Pin.board.PA10, 3)
    
    ## motor2 Motor object 2.
    motor2 = MotorDriver(pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Pin.board.PC1, 5)
    
    motor2.enable()
    motor2.set_duty_cycle(0)

