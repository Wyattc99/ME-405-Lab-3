"""!
@file plottingtask.py
The PC program to communicate to Nucleo through the serial port. This
program also plots the data received through the serial port in a
Encoder Ticks, vs Time plot
@author Jacob Wong
@author Wyatt Conner
@author Jameson Spitz
@date   2-Feb-22
@copyright by Jacob Wong all rights reserved
"""

import serial
import time
from matplotlib import pyplot

## Empty Lists and string for manipulating data from serial port time data
time_data_A = [] 
## Empty Lists and string for manipulating data from serial port position data
pos_data_A= []
## Empty Lists and string for manipulating data from serial port time data
time_data_B = [] 
## Empty Lists and string for manipulating data from serial port position data
pos_data_B = []
## Empty Lists and string for manipulating data from serial port overall data
string = ''
## Empty Lists and string for manipulating data from serial port int values of ticks data
ticks = []

## This is an empty array used to store position data from encoder A
pos_A_count = []
## This is an empty array used to store position data from Timer B
time_A_count = []
## This is an empty array used to store position data from encoder B
pos_B_count = []
## This is an empty array used to store position data from Timer B
time_B_count = []

# Begins communication with Serial Port COM27
with serial.Serial('COM6', 115200) as s_port:
    
        time.sleep(.1)
        # CTRL-C
        s_port.write(b'\x03')
        time.sleep(.1)
        # CTRL-D
        s_port.write(b'\x04')
        time.sleep(.1)
        # Sets Desired Ticks to 16000
        s_port.write (b'16000\r')
        time.sleep(.1)
        # Sets Proportional Gain to 16000
        s_port.write (b'40\r')
        time.sleep(.5)
        # Sets Desired Ticks to 16000
        s_port.write (b'16000\r')
        time.sleep(.1)
        # Sets Proportional Gain to 16000
        s_port.write (b'40\r')
        #time.sleep(5)
        
        ## This varuable represents the data read up until next set of data
        data = s_port.read_until(b'Time')      
        
        time.sleep(.1)
        # Flushes buffer until prompt
        # s_port.read_until(b'\nTime List A\n')
        time.sleep(.1)
        ## Writes time data as a string to 'data1'
        time_data_A = s_port.read_until(b'Encoder')
        time.sleep(.1)
        ## Writes ticks data as a string to 'data2'
        pos_data_A = s_port.read_until(b'Time')
        time.sleep(.1)
        ## Writes time data as a string to 'data1'
        time_data_B = s_port.read_until(b'Encoder')
        time.sleep(.1)
        ## Writes ticks data as a string to 'data2'
        pos_data_B = s_port.read_until(b'Data')
        time.sleep(.1)
        
        ## Time A data in a string format
        time_data_stringA = time_data_A.decode('Ascii')
        ## Ticks A data in a string format
        pos_data_stringA = pos_data_A.decode('Ascii')
        ## Time B data in a string format
        time_data_stringB = time_data_B.decode('Ascii')
        ## Ticks B data in a string format
        pos_data_stringB = pos_data_B.decode('Ascii')
        
        
        # Converts Time A data to intergers
        for i in time_data_stringA:
            if(i.isnumeric()):
                string += i
            elif(i == '\n'):
                try:
                    time_A_count.append(int(string)/1000)
                    string = ''
                except:
                    pass
                
        # Converts Position A data to intergers        
        for i in pos_data_stringA:
            if(i.isnumeric()):
                string += i
            elif(i == '\n'):
                try:
                    pos_A_count.append(int(string))
                    string = ''
                except:
                    pass
        
        # Converts Time B data to intergers
        for i in time_data_stringB:
            if(i.isnumeric()):
                string += i
            elif(i == '\n'):
                try:
                    time_B_count.append(int(string)/1000)
                    string = ''
                except:
                    pass
                
        # Converts Position B data to intergers       
        for i in pos_data_stringB:
            if(i.isnumeric()):
                string += i
            elif(i == '\n'):
                try:
                    pos_B_count.append(int(string))
                    string = ''
                except:
                    pass
        

## Creates and formats 'Encoder Ticks vs Time' plot
font = {'fontname':'Times New Roman'}
pyplot.plot(time_A_count, pos_A_count, '-ok', time_B_count, pos_B_count, '-ob')
pyplot.title('Encoder Ticks vs. Time', font)
pyplot.xlabel('Time, t [s]', font)
pyplot.ylabel('Encoder Ticks', font)
pyplot.grid()
pyplot.legend(['Motor 1', 'Motor 2'])

if __name__ == "__main__":
    print('')