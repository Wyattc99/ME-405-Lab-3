"""!
@file main.py
    This file uses an inter-task method to run two motors in a position 
    control loop simultaneously at a specified frequency. The program utilizes
    shared and queued variables to collect motor data and print it once
    the control loop is terminated.

@author JR Ridgely
@author Wyatt Conner
@author Jameson Spitz
@author Jacob Wong
@date   2022-Feb-09 Last updated
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
    Task which facilitates the motor position control method and records
    motor 1 data in a queue. The task then prints the data which is controlled
    by a generator.
    """
    
    ## State varible used to signal program whether to collect data, print
    #  data, or terminate program.
    state = 0
    
    while True:
        
        ## Updates Current Time
        if(state == 0):
            
            # Runs position control function from positioncontrol.py
            control_A.position_control()
        
            ## Current time at which the position data is collected
            current_time_A = time.ticks_diff(time.ticks_ms(), start_time)
            
            if current_time_A > 5000:
                state = 1
            
            # Collect time list data if the queue is not full
            if time_list_A.full() == False:
                # Creates a list of Time data
                time_list_A.put(current_time_A)

            # Collect position data if the queue is not full                
            if Position_A.full() == False:
                # Creates a list of Time data
                Position_A.put(enc_A.get_position())
            else:
                pass
        
        # States to print data
        elif state == 1:
            print('\nTime List A\n')
            state = 2
            
        elif state == 2:
            if time_list_A.any():
                print(time_list_A.get())
            else:
                state = 3
                
        elif state == 3:
            print('\nEncoder Position A\n')
            state = 4
            
        elif state == 4:
            if Position_A.any():
                print(Position_A.get())
            else:
                state = 5
                
        elif state == 5:
            print('\nTime List B\n')
            state = 6
            
        elif state == 6:
            if time_list_B.any():
                print(time_list_B.get())
            else:
                state = 7
                
        elif state == 7:
            print('\nEncoder Position B\n')
            state = 8
            
        elif state == 8:
            if Position_B.any():
                print(Position_B.get())
            else:
                state = 9
        
        # Terminate program with share0 flag
        elif (state == 9):
            print('Data has been collected')
            state = 10
            share0.put(1)
        elif (state == 10):
            pass

        yield (0)
        
def system_2 ():
    """!
    Task which facilitates the motor position control method and records
    motor 1 data in a queue. The task then prints the data which is controlled
    by a generator.
    """
    
    ## State varible used to signal program whether to collect data, print
    #  data, or terminate program.
    state = 0
    
    while True:

        if (state == 0):
            
            # Runs position control function from positioncontrol.py
            control_B.position_control()
            
            ## Current time at which the position data is collected
            current_time_B = time.ticks_diff(time.ticks_ms(), start_time)
            
            if current_time_B > 5000:
                state = 1
            
            if time_list_B.full() == False:
                # Creates a list of Time data
                time_list_B.put(current_time_B)
            
            # Collect Position data if queue is not full
            if Position_B.full() == False:
                Position_B.put(enc_B.get_position())
                
            else:
                break
            
        elif (state == 1):
            pass
            
        yield (0)

def user_task ():
    
    """!
    Task which puts things into a share and a queue.
    """
    yield(0)

# This code creates important Queue and Share variables, then starts the tasks. 
# The tasks run until the motors have reached desired position within 5 seconds
# and data has been printed, at which time the scheduler stops and printouts 
# show diagnostic information about the tasks, share, and queue.
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
    
    # Asking user to specify set point and gain for motor 1
    print('motor 1')
    control_A.set_point()
        
    control_A.set_gain()
    
    # Asking user to specify set point and gain for motor 2
    print('motor 2')
    control_B.set_point()
        
    control_B.set_gain()
    
    # Initilzing Share Objects
    
    # Shares
    # def __init__ (self, type_code, thread_protect = True, name = None):
    
    # Queue
    # def __init__ (self, type_code, size, thread_protect = True, 
    #              overwrite = False, name = None):
        
    ## Creates the position Queue object
    Setpos_A = task_share.Queue('i', True, name = 8)
    
    ## Creates the position of motor 1 Queue object
    Position_A = task_share.Queue('i', size = 250, thread_protect = False,
                                  overwrite = False, name = 1)

    ## Creates the position of motor 2 Queue object
    Position_B = task_share.Queue('i', size = 250, thread_protect = False,
                                  overwrite = False, name = 2)

    ## Creates the time storage Queue for motor 1
    time_list_A = task_share.Queue('i', size = 250, thread_protect = False,
                                  overwrite = False, name = 5)
    
    ## Creates the time storage Queue for motor 2
    time_list_B = task_share.Queue('i', size = 250, thread_protect = False,
                                  overwrite = False, name = 6)
    
    ## Start time to reference relative time of data recording
    start_time = time.ticks_ms()
    
    ## Counter to measure number of runs through queue
    counter_2 = 0
    
    ## Counter to measure number of runs through queue
    counter_1 = 0
    
    #>>> Start of Example Code From Ridgely<<<

    # Create a flag as a Shared variable to signal the schedular should stop
    share0 = task_share.Share ('i', thread_protect = False, name = "Share 0")
    
    #q0 = task_share.Queue ('L', 16, thread_protect = False, overwrite = False,
                          # name = "Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
 
    task1 = cotask.Task (system_1, name = 'Task_1', priority = 1, 
                             period = 50, profile = True, trace = False)
 
    
    task2 = cotask.Task (system_2, name = 'Task_2', priority = 1, 
                             period = 50, profile = True, trace = False)
  
        
    # Add tasks to cotask schedular list
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if the flag
    # variable share0 has been set to 1 by the task state machine after 
    # printing the data.
    vcp = pyb.USB_VCP ()
    vcp.read()
    
    while share0.get() != 1:
        cotask.task_list.pri_sched()

        
    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')