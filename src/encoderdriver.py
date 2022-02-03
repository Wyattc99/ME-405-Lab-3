"""!
@file encoderdriver.py
This file configures Nucleo pins, timers, and channels for so that it can send voltage to a motor.
Can send a PWM duty cycle to the motor to control how fast the motor spins. Uses a L6206 motor shield to control motor direction.
@author Jacob Wong
@author Wyatt Conner
@author Jameson Spitz
@date   26-Jan-22
@copyright by Jacob Wong all rights reserved
"""

import pyb
import time


class EncoderDriver():
    """!
    Initializes encoder pins, timer, and channel. Allows for multiple encoders to be configured each with different
    timers and pins. Can update motor position by updating how many ticks are seen by the encoder.
    """
# pins for the encoders
# pinINB6 = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
# pinINB7 = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)

# pinA1 = pyb.Pin.board.PB6
# pinA2 = pyb.Pin.board.PB7
# pinB1 = pyb.Pin.board,PC6
# pinB2 = pyb.Pin.board,PC7

    def __init__(self, pinA1, pinA2, timer):
        
        """!
        Initialize pins, timers and channels.
        @param pinA1 First pin connected to encoder.
        @param pinA2 Second pin connected to encoder.
        @param timer Sets up timer for encoder pins.
        """
        
        ## sets pinA1 to input pin.
        self.pinA1 = pyb.Pin(pinA1, pyb.Pin.IN)
        
        ## sets pinA2 to input pin.
        self.pinA2 = pyb.Pin(pinA2, pyb.Pin.IN)
        
        ## sets up timer for pins with specified period.
        self.tim4 = pyb.Timer(timer, period = 65535, prescaler = 0)
        
        ## Creates timer channel 1 object for pinA1.
        self.t4ch1 = self.tim4.channel(1, pyb.Timer.ENC_AB, pin = self.pinA1)
        
        ## Creates timer channel 1 object for pinA1.
        self.t4ch2 = self.tim4.channel(2, pyb.Timer.ENC_AB, pin = self.pinA2)
        
        ## per is the tick count at which the encoder resets.
        self.per = 65535
        
        ## old_tick tracks the previous tick count to count position.
        self.old_tick = 0
        
        ## position stores how many ticks the encoder has seen.
        self.position = 0

        
    def update_delta(self):
        
        """!
            Updates encoder value by adding delta, the change in position, to our position variable.
            Handles overflow by adding or subtracting the period from delta when delta exceeds half the period.
        """
        
        ## new_tick stores the current tick valus the encoder reads.
        new_tick = self.tim4.counter()

        ## delta tracks the change in position since the last time the encoder updated.
        delta = new_tick - self.old_tick
        
        self.old_tick = new_tick

        if(abs(delta) >= self.per/2):    #handles overflow if delta is greater than half the period
            if(delta > 0):
                delta -= self.per        #if delta is positive, subtract period
            else:
                delta += self.per        #if delta is negative, add period
                
        self.position += delta
        time.sleep(.1)
            
    def get_position(self):
        
        """!
            Returns the current position of encoder.
        """
        
        return self.position
    
    def set_position(self, val):
        
        """!
            Overwrites the old position of encoder and sets it to a new position.
            @param val The position encoder is set too.
        """
        
        self.position = val
        
    
if __name__ == "__main__":
    
    ## my_encoder1 Encoder object 1.
    #my_encoder1 = EncoderDriver(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)
    
    ## my_encoder2 Encoder object 2.
    my_encoder2 = EncoderDriver(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)
    
    while True:
        my_encoder2.update_delta()
        print(my_encoder2.get_position())
