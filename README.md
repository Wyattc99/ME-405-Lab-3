# ME - 405 Lab 2
## Authors: Wyatt Conner, Jameson Spitz, Jacob Wong
### This is the lab 3 code for ME 405 in which we produce a position control system of a motor and encoder pair through the serial port.
 
## Scheduler / Main
In this Lab we created a main file that acted as a scheduler for our tasks
which controls two motors and encoders for a position control. This was done
with a generator that would command the control task to run at a certain
frequency. The scheduler controls both motors and encoders with seperate motor and
encoder objects that are passed into seperate objects of the controller task. 

## Control Task
The motors and encoders were controlled through a task called Position Control Task, which
would allows the users to set the set point and gain of the controller. With
that information the controller can then grab encoder position calculate how
far the motor is off from the desired position, multiply that error by the
gain and produce a duty cycle to send to that motor to correct its position.

## Plotting Task
The plotting task is the code intended to be used on the PC to command the
microcontroller what to do. The plotting tasks writes the commands needed to
controller task to set the desired set point and gain values. From there the 
Main file will manage the control of the motors and collection of data.
Once the data collection is complete main will print the data in a specific format.
This is outputted to the serial port where the Plotting Task can read the
data and plot it, so the microcontroller does not have to. 

# 200ms Period Plot
![200ms Period Plot](/Plts/MotorResponse_200ms.png)

The lowest period we were able to achieve was 200ms, which is really long
to what we should have been able to achieve. This period was sufficent enough
to control the position of motor as seen in the graph above. The response looks
similar to that of a first order response that appears critically damped. 

#1000ms Period Plot
![1000ms Period Plot](/Plts/MotorResponse_1000ms.png)

We continued to increase our period of the controller tasks to see how it affects
the control of position on the motor. As we can see in the graph above a
period of the controller is 1000ms which is 1 second. This causes issues
of over shooting and saturation which leads the system to be nearly unstable.
If the period where to be larger than 1000ms it is more than likely the system
would become unstable. 