"""
Project 1: Elevator 
Elevators allow you to travel through different levels of a building in an easier, more comfortable and faster way. They are sometimes called classic elevators, building elevators, passenger elevators or building elevators. The minimum elevator size is approximately 700 x 1,300 (W x D) millimeters versus a standard elevator size of 1,100 x 1,400 (W x D) millimeters. The elevator speed varies between 25 and 250 centimeters per second, although high performance devices can reach 70 kilometers per hour. An elevator is made up of several parts including: 

A cabin:
Also called a cage, it represents the compartment that carries the passenger through the floors of a building when the elevator is moving. It consists of walls, either steel or glass, supported by a robust metal structure.  

Landing gates:
They are the device intended to isolate the car to better protect the passengers during the transport. They close and open together with the cabin doors thanks to an automatic synchronization mechanism, known as a retractable saber. Between the two doors, the control always comes from the cab doors. In other words, the landing doors are only unlocked by the cab doors, which are activated by their own motor. Closing the doors is done by a counterweight. 

A control panel:
It allows you to call or direct the car. To do this, it has several buttons: call buttons, on each level of the building, and floor buttons, in the car itself. Its role is to transmit your requests directly to the control cabinet, the electronic brain of your elevator. If elevator companies can propose a wide range of elevators, the layout of the control panels must always be done according to the NF EN 81-70 standard. Thus, each inscription of the buttons must be in relief and the remote alarm button must be easily identifiable to warn the helpers in case of emergency. 

A control box:
It receives all the information from the control panel and the various sensors installed on your elevator before transmitting the orders to the machinery. When the car arrives for example near the first floor, it is this cabinet that orders the motor to slow down before stopping. It is also mounted in series with the landing doors and the on-board safety systems: if one element fails, the whole mechanism goes into emergency stop, which prevents any anomaly. 

The goal of this project is to program (simulate) the operation of an elevator (n floors) in Python. 

The functioning of an elevator is described as follows:

1. User:
• The user arrives in front of the elevator, moves forward and presses the button
• The elevator opens and the user gets on the elevator
• The user presses the number of the floor he/she is going down to
• The elevator closes and performs the trip
• During this moment another user could ask for the elevator

2. Elevator:
• As long as it is not called anywhere, the elevator remains stationary;
• When called, the elevator starts moving, to move to the floor (landing) where it
is requested;
• When it moves, it can be called to another floor, or it can be asked to go to a
given floor (case of the passenger who enters in the elevator) ;
• The movement of the elevator obeys a particular policy, to avoid the
phenomenon of "starvation": as long as it has to go (called or sent) higher, it goes up (and
respectively). It goes down only when it does not need to go up anymore. This is why there
are buttons on the landings to go up and down.

This project consists in writing a program in python that will simulate the operation of an
elevator that will serve at least 8 floors(level). The maximum number of passengers that
the elevator can take is 8, with a total weight of 1600kg.

"""

#Necessary imports for randomize the activity.
import threading
import time
#Import of classes created for every aspect of the simulation and GUI.
from window import Window
from elevator import Elevator
from floor import Floor
from building import Building
import random
from screen_info import ScreenInfo

#Maximum number of calls.
nb_calls = 10000

<<<<<<< HEAD
acceleration = 1
=======
#Time of execution.
acceleration = 0.00001
>>>>>>> 34cffd66a447c2d8133f56b1ccf395d63e117554

def GUI_th(window):
    window.draw()

# Used to randomize the calls from the floors.
# A second thread is used for this loop.
def calls(floors, elevator):
    # loop nb_calls times
    for i in range(nb_calls):
        # A floor is chosen ramdomly.
        floor_nb =  random.randint(0,7)
        # If the floor does not have people queuing, new people is created .
        if not floors[floor_nb].has_people():
            # If new people is created the elevator is called.
            floors[floor_nb].create_people()
            # Use to wait at the beginning.
            if i == 0:
                time.sleep(1*acceleration)
            if floors[floor_nb].has_people():
                floors[floor_nb].call_elevator(elevator)
                # Wait between calls.
                time.sleep(2*acceleration)
        # If the window is closed, this thread dies
        if not elevator.is_working:
            break
        

# controlled calls (floor class should be modified)
# def calls(floors, elevator):
#     for floor in floors:
#         if len(floor.people) > 0:
#             elevator.external_request(floor.number)


if __name__ == '__main__':
    # Creating window.
    window = Window()

    # Creating background (building).
    building = Building(window)
    window.add_object(building, 1)

    # Creating floors.
    floors = []
    for i in range(8):
        floors.append(Floor(window, i))
        floors[-1].acceleration(acceleration)
        window.add_object(floors[-1], 2)

    # Create screen info.
    screen_info = ScreenInfo(window)
    window.add_object(screen_info, 9)

    # Create elevator
    elevator = Elevator(window, floors, screen_info, 0)
    elevator.acceleration(acceleration)
    window.add_object(elevator, 3)
        
    
    # Creating thread for the calling on the floors.
    calling_thread = threading.Thread(target=calls, args=(floors,elevator))
    calling_thread.start()

    # The thread for the GUI is the principal thread.
    GUI_th(window)
    elevator.is_working = False


# Here you can find details from the rest of the classes:

# [For `person.py`, click here](./person.html)

# [For `people_group.py`, click here](./people_group.html)

# [For `elevator.py`, click here](./elevator.html)

# [For `floor.py`.py, click here](./floor.html)

# [For `building.py`, click here](./building.html)

# [For `screen_info.py`, click here](./screen_info.html)

# [For `window.py`, click here](./window.html)

#for a detalied look at the [Repo, click here](https://github.com/AgustinCartaya/Python-elevator)
