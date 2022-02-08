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
## Empty Lists and string for manipulating data from serial port int values of time data
time_count = []
## Empty Lists and string for manipulating data from serial port int values of ticks data
ticks = []

# Begins communication with Serial Port COM27
with serial.Serial('COM27', 115200) as s_port:
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
        time.sleep(.5)
        # Eliminates text from output buffer
        s_port.reset_output_buffer()
        time.sleep(.1)
        # Flushes buffer until prompt
        s_port.read_until(b'A')
        time.sleep(.1)
        ## Writes time data as a string to 'data1'
        time_data_A = s_port.read_until(b'P')
        time.sleep(.1)
        ## Writes ticks data as a string to 'data2'
        pos_data_A = s_port.read_until(b'T')
        time.sleep(.1)
        ## Writes time data as a string to 'data1'
        time_data_B = s_port.read_until(b'P')
        time.sleep(.1)
        ## Writes ticks data as a string to 'data2'
        pos_data_B = s_port.read_until(b'T')
        time.sleep(.1)
        # Decodes both strings to ASCII
        
        # ## Time data in a string format
        # time_data_stringA = time_data_A.decode('Ascii')
        # ## Ticks data in a string format
        # pos_data_stringA = pos_data_A.decode('Ascii')
        # print(time_data_stringA)
        # print(pos_data_stringA)
        
        # # Removes extraneous characters from data_string 1
        # data_string1.strip('\n')
        # data_string1.strip(' ')
        # data_string1.strip('[')
        # data_string1.strip(']')
        
        # # Removes extraneous characters from data_string 2
        # data_string2.strip('\n')
        # data_string2.strip(' ')
        # data_string2.strip('[')
        # data_string2.strip(']')
        
        # # Converts data_string1 to list called 'time_count'
        # for i in data_string1:
        #     if(i.isnumeric()):
        #         string += i
        #     elif(i == ',' or i == ']'):
        #         time_count.append(int(string)/1000)
        #         string = ''
        
        # # Converts data_string2 to list called 'ticks'
        # for i in data_string2:
        #     if(i.isnumeric()):
        #         string += i
        #     elif(i == ',' or i == ']'):
        #         ticks.append(int(string))
        #         string = ''

# # Prints final data lists in command window
# print('\nTime:\n', time_count)                   
# print('\nTicks:\n', ticks)

# ## Creates and formats 'Encoder Ticks vs Time' plot
# font = {'fontname':'Times New Roman'}
# pyplot.plot(time_count, ticks, '-ok')
# pyplot.title('Encoder Ticks vs. Time', font)
# pyplot.xlabel('Time, t [s]', font)
# pyplot.ylabel('Encoder Ticks', font)
# pyplot.grid()

if __name__ == "__main__":
    print('')