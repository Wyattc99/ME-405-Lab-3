"""!
@file main.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@author Wyatt Conner
@author Jameson Spitz
@author Jacob Wong
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
import time

from positioncontrol import PositionControlTask
from motordriver import MotorDriver
from encoderdriver import EncoderDriver



def system_1 ():
    """!
    Task which puts things into a share and a queue.
    """
    
    while True:

        # Runs position control function from positioncontrol.py
        control_A.position_control()
        
        ## Current time the data is collected
        current_time_A = time.ticks_diff(time.ticks_ms(), start_time)
        
        ## Updates Current Time
        if time_list_A.full() == False:
            # Creates a list of Time data
            time_list_A.put(current_time_A)
            timeA = current_time_A
            #print('Time =', timeA)

            
        if Position_A.full() == False:
            # Creates a list of Time data
            Position_A.put(enc_A.get_position())
            posA = enc_A.get_position()
            #print('Position =', posA)
        else:
            break
            
        #print('sys 1')
        yield (0)
        
def system_2 ():
    

    while True:

        # Runs position control function from positioncontrol.py
        control_B.position_control()
        
        ## Current time the data is collected
        current_time_B = time.ticks_diff(time.ticks_ms(), start_time)
        
        ## Updates Current Time
        if time_list_B.full() == False:
            # Creates a list of Time data
            time_list_B.put(current_time_B)
       
            
        if Position_B.full() == False:
            # Creates a list of Time data
            Position_B.put(enc_B.get_position())
        else:
            break
            
        #print('sys 2')
        yield (0)

def user_task ():
    """!
    Task which puts things into a share and a queue.
    """
    yield(0)

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
           'Press ENTER to stop and show diagnostics.')
    
    
    #>>>>> Initlizing Class Personal Objects <<<<<<

    ## Creates the motor object for motor B
    motor_B = MotorDriver(pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Pin.board.PC1, 5)

    ## Creates the motor object for motor A
    motor_A = MotorDriver(pyb.Pin.board.PB4, pyb.Pin.board.PB5, pyb.Pin.board.PA10, 3)

    ## Creates the encoder object for encoder B
    enc_B = EncoderDriver(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)

    ## Creates the encoder object for encoder A
    enc_A = EncoderDriver(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)

    ## Create the position control object for system A
    control_A = PositionControlTask(motor_A, enc_A)

    ## Creates the position control object for system B
    control_B = PositionControlTask(motor_B, enc_B)
    
    print('motor 1')
    control_A.set_point()
        
    control_A.set_gain()
    
    print('motor 2')
    control_B.set_point()
        
    control_B.set_gain()
    
    # Initilzing Share Objects
    
    # Shares
    # def __init__ (self, type_code, thread_protect = True, name = None):
    
    # Queue
    #def __init__ (self, type_code, size, thread_protect = True, 
    #              overwrite = False, name = None):
    ## Creates the position Queue object
    Setpos_A = task_share.Queue('i', True, name = 008)
    ## Creates the position Queue object
    Position_A = task_share.Queue('i', size = 25, thread_protect = False,
                                  overwrite = False, name = 001)

    ## Creates the position share object
    Position_B = task_share.Queue('i', size = 25, thread_protect = False,
                                  overwrite = False, name = 002)

    # Initilzing variables
    time_list_A = task_share.Queue('i', size = 25, thread_protect = False,
                                  overwrite = False, name = 005)
    time_list_B = task_share.Queue('i', size = 25, thread_protect = False,
                                  overwrite = False, name = 006)
    start_time = time.ticks_ms()
    counter_2 = 0
    counter_1 = 0
    #>>> Start of Example Code From Ridgely<<<

    # Create a share and a queue to test function and diagnostic printouts
    #share0 = task_share.Share ('h', thread_protect = False, name = "Share 0")
    #q0 = task_share.Queue ('L', 16, thread_protect = False, overwrite = False,
                          # name = "Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
 
    task1 = cotask.Task (system_1, name = 'Task_1', priority = 1, 
                             period = 200, profile = True, trace = False)
 
    
    task2 = cotask.Task (system_2, name = 'Task_2', priority = 1, 
                             period = 200, profile = True, trace = False)
  
        
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    vcp.read()
    while not vcp.any ():
    #while True:
        try:
            cotask.task_list.pri_sched ()
            
        except StopIteration:
            
            print('\nTime List A\n')
            while time_list_A.any():
                print(time_list_A.get())
                
            print('\nEncoder Position A\n')
            while Position_A.any():
                print(Position_A.get())
                
            print('\nTime List B\n')
            while time_list_B.any():
                print(time_list_B.get())
                
            print('\nEncoder Position B\n')
            while Position_B.any():
                print(Position_B.get())
                
            print('\nData has been collected\n')
                
            break
        
    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')