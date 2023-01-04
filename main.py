import threading
import time
from window import Window
from elevator import Elevator
from floor import Floor
from building import Building
import random
from screen_info import ScreenInfo

# max number of calls

nb_calls = 10000

acceleration = 1

def GUI_th(window):
    window.draw()

# used to randomize the calls from the floors
# a secon thread is used for this loop
def calls(floors, elevator):
    # loop nb_calls times
    for i in range(nb_calls):
        # a floor is chosen ramdomly
        floor_nb =  random.randint(0,7)
        # if the floor does not have people queuing, new people is created 
        if not floors[floor_nb].has_people():
            # if new people is created the elevator is called
            floors[floor_nb].create_people()
            # use to wait at the beginning
            if i == 0:
                time.sleep(1*acceleration)
            if floors[floor_nb].has_people():
                floors[floor_nb].call_elevator(elevator)
                # wait between calls
                time.sleep(2*acceleration)
        # if the window is closed this thread died
        if not elevator.is_working:
            break
        

# controlled calls (floor class should be modified)
# def calls(floors, elevator):
#     for floor in floors:
#         if len(floor.people) > 0:
#             elevator.external_request(floor.number)


if __name__ == '__main__':
    # creating window
    window = Window()

    # creating background (building)
    building = Building(window)
    window.add_object(building, 1)

    # creating floors
    floors = []
    for i in range(8):
        floors.append(Floor(window, i))
        floors[-1].acceleration(acceleration)
        window.add_object(floors[-1], 2)

    # create screen info
    screen_info = ScreenInfo(window)
    window.add_object(screen_info, 9)

    # create elevator
    elevator = Elevator(window, floors, screen_info, 0)
    elevator.acceleration(acceleration)
    window.add_object(elevator, 3)
        
    
    # creatin thread for the calling on the floors
    calling_thread = threading.Thread(target=calls, args=(floors,elevator))
    calling_thread.start()

    # the thread for the GUI is the principal thread
    GUI_th(window)
    elevator.is_working = False
