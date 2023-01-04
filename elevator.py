import pygame 
import os
from people_group import PeopleGroup
import threading
 
# === Class that models a group of people from the class `people_group.py` and contains the neccesary functions to desing and control the the elevator===

# [For people_group.py class documentation, click here](./people_group.html).

class Elevator:
    lock = threading.Lock()

    # Time (in seconds) to travel from a floor to another.
    TIME_MOVING = 1
    # Time (in seconds) to stay on a floor with the door opened.
    TIME_OPEN = 1

    #Maximum supported charge of the elevator, in kilograms. According to the constraints of the project.
    MAX_CHARGE = 1600
    #Maxinum number of people supported inside the elevator according to the project constraints.
    MAX_PEOPLE = 8

    #Image assets of the elevator in the GUI.
    IMG_EMPTY = "IMG_EMPTY"
    IMG_FULL = "IMG_FULL"

    """
    Possible States of the elevator:

   -STATE_OPEN: Elevator is charging/discharging in a floor. Doors Open.

   -STATE_MOVING : Elevator is moving.

   -STATE_WATING: Elevator is waiting for a call.
   """
    STATE_MOVING = "MOVING"
    STATE_OPEN = "OPEN"
    STATE_WATING = "CLOSE"

    #Distance in Pixels that the elevator moves in order to go from one floor to another.
    DISTANCE_FLOOR = 94.0

    def __init__(self, window, floors, screen_info, current_floor=0):
        self.window = window

        # Initialization of all parameters of a floor.
        self.current_floor = current_floor
        self.direction = 0
        self.floors = floors
        self.requested_floor = 0

        # Initialization of the state of the elevator.
        self.current_state = self.STATE_WATING
        self.open_counter = 0

        # Initialization of elevator image asset.
        self.current_img = self.IMG_EMPTY
        self.img_elevator = {}

        # Initialization of people group and queue of calls.
        self.queue = []
        self.people = PeopleGroup()
        self.entered_people = 0
        self.exit_people = 0

        # Initial Position.
        self.pos_y = 24 + self.DISTANCE_FLOOR*self.current_floor
        self.pos_x = 300
        self.moving_counter = 0

        # Initialization of the screen information.
        self.screen_info = screen_info

        #Flag used to stop the application.
        self.is_working = True

        # If this parameter is true, the elevator will print in the terminal all the steps.
        self.talkative = True

        # Emergency call.
        self.emergency = False

        # This charges elevator.
        self.init_img_elevator()

    # Method to obtain external calls from the floors
    def external_request(self, floor_number):
        self.talk("floor called %d " % floor_number)
        self.__request(floor_number)

    # Method to obtain internal calls from the inside of the elevator, either a floor from the control pannel, either an Emergency call.
    def internal_request(self, floor_number):
        if floor_number < 0:
            self.talk("EMERGENCy CALLED !!!!!!!!!!!", True)
            self.emergency = True
        self.talk("internal call %d " % floor_number)
        self.__request(floor_number)

    # === Queue calls ===
    
    # This function can be accessed by two threads: the elevator_th in the main thread and floors_th.
    # However, in order to avoid concurrence, it is accessible by only one thread at a time.
    def __request(self, floor_number):
        self.lock.acquire()
        self.queue.append(floor_number)
        self.lock.release()

    # === Function to change the state of the elevator. ===

    # Action timing will depend on the state. E.g.: if it is opened
    # then uses the TIME.OPEN, if it is moving, then TIME.MOVING
    def change_state(self, state):
        self.talk("Stated changed: %s ---> %s\n\n"%(self.current_state, state))
        if state == self.STATE_OPEN:
            self.open_counter = self.TIME_OPEN
        elif state == self.STATE_MOVING:
            self.moving_counter = self.TIME_MOVING

        if state != self.TIME_MOVING and self.current_floor == self.requested_floor:
            self.direction = 0

        self.current_state = state

    # === Core function of the elevator operation. ===

    # Control the states of each step of the operation and respond to the calls amde from external or internal input.
    def serve(self):
        # First, check if the elevator is open to decrease the opening time.
        if self.current_state == self.STATE_OPEN:
            self.open_counter = self.open_counter - 1/self.window.FPS
            if self.open_counter <= 0:
                if self.direction == 0:
                    self.change_state(self.STATE_WATING)
                else:
                    self.change_state(self.STATE_MOVING)
                self.floors[self.current_floor].close_door()

        # Check if the elevator is waiting and the queue is not empty, so it can respond to the first call.
        elif self.current_state == self.STATE_WATING and len(self.queue)>0:
            self.lock.acquire() #
            self.requested_floor = self.queue.pop(0)
            self.lock.release() #
            self.talk("(1) call receaved from floor : %d" % self.requested_floor)
            
            if self.requested_floor == self.current_floor:
                self.talk("(1.1) called from the same floor, opening the door")
                self.open_door()
            else:
                self.direction = self.get_direction(self.requested_floor)
                self.change_state(self.STATE_MOVING)

        # Check if the elevator reach a requested floor while is moving.
        elif self.current_state == self.STATE_MOVING:
            # Activity of the elevator on a floor.
            if  self.moving_counter <= 0:
                self.moving_counter = 0
                self.current_floor = self.current_floor + self.direction
                self.talk("(2) arrived to floor : %d" % self.current_floor)                    
                if self.current_floor == self.requested_floor or self.current_floor in self.queue:
                    self.open_door()                        
                else:
                    self.change_state(self.STATE_MOVING)
            else:
                self.moving_counter = self.moving_counter - 1/self.window.FPS

    #===Up or down.===
    
    # Return the direction of the elevator. Ascending or Descending.
    def get_direction(self, requested_floor):
        res = self.current_floor - requested_floor
        if res < 0:
            return 1
        else :
            return -1
    # === Weight Restrictions: ===

    # return true if the elevator cannot take more people
    def is_full(self, p_weight=0):
        return ((len(self.people) == self.MAX_PEOPLE) or (self.people.get_weight()+p_weight >= self.MAX_CHARGE))

    #=== Operations in a floor: ===

    # Set of necessary actions when the elevator reaches a floor.

    #Opens the door.
    def open_door(self):
        self.change_state(self.STATE_OPEN)

        self.talk("(3) opening the door on floor %d" % self.current_floor)

        # Removing people going out first, as a rule of thumb.
        people_going_out = self.people.get_exit_floor(self.current_floor)
        self.people.remove_sub_group(people_going_out)
        self.exit_people = self.exit_people + people_going_out.get_nb()
        self.lock.acquire()
        self.queue = list(filter((self.current_floor).__ne__, self.queue))
        self.lock.release()
        self.talk("(4) Nb people went out %d " % people_going_out.get_nb())

        # Then, obtaining the people that is entering just if it is possible to allow more people inside due to the constraints: Weight and Number of people in the cabin.
        if not self.is_full():
            new_people = self.floors[self.current_floor].open_door(people_going_out)

            #Internal command.
            nb_people_entered = 0
            for p in new_people:
                # if p.exit_floor != self.current_floor:
                if not self.is_full(p.weight):
                    self.people.add_person(p)
                    nb_people_entered = nb_people_entered + 1
                    self.internal_request(p.exit_floor)
                else:
                    self.floors[self.current_floor].over_weight(new_people.get_last(nb_people_entered))
                    break
            self.entered_people = self.entered_people + nb_people_entered
            self.talk("(5) Nb people entered %d " % nb_people_entered)
            
            # The elevator should be called again for the people that could not enter
            if nb_people_entered <  len(new_people):
                self.talk("(5.1) Nb people entered not entered %d" % (nb_people_entered - len(new_people)))
                self.floors[self.current_floor].call_elevator(self)

        else:
            #Call gets queued when not everybody could enter the cabin.
            self.talk("(5) Cannot take more people, queued call")
            self.floors[self.current_floor].call_elevator(self)

        self.talk("(6) People in the elevator %d, current floor: %d \n\n" % (self.people.get_nb(), self.current_floor))

    # Initializing the images of the elevator.
    def init_img_elevator(self):
        # Empty elevator assets.
        img_empty = pygame.image.load(os.path.join('src','img', 'elevator_empty.png'))
        img_empty = pygame.transform.smoothscale(img_empty,(55, 95))
        # Full elevator assets.
        img_full = pygame.image.load(os.path.join('src','img', 'elevator_full.png'))
        img_full = pygame.transform.smoothscale(img_full,(55, 95))

        self.img_elevator = {self.IMG_EMPTY : img_empty,
                            self.IMG_FULL: img_full}

    # Calculate the position of the elevator.
    def calc_y_pos(self):
        if self.moving_counter > 0:
            self.pos_y = 22 + self.DISTANCE_FLOOR*self.current_floor + (1 - self.moving_counter/self.TIME_MOVING) * self.direction * self.DISTANCE_FLOOR 
    
    # Draw the elevator on the screen
    def draw(self):
        if not self.emergency:
            self.serve()
            self.calc_y_pos()

        if(len(self.people) > 0):
            self.window.screen.blit(self.img_elevator[self.IMG_FULL], (self.pos_x, self.pos_y))
        else:
            self.window.screen.blit(self.img_elevator[self.IMG_EMPTY], (self.pos_x, self.pos_y))

        # Refreshing information for the most up to date info about the state of the system.
        self.screen_info.refresh({"queue":self.queue,
                        "current_floor":self.current_floor,
                        "requested_floor":self.requested_floor,
                        "people":self.people,
                        "moving":self.direction,
                        "current_state": self.current_state,
                        "emergency": self.emergency})

    # Used to print on the terminal each of the actions of the elevator.
    def talk(self, comment, important=False):
        if self.talkative or important:
            print("Elevator: ", comment)
        
    def acceleration(self, mult):
        self.TIME_MOVING = self.TIME_MOVING * mult
        self.TIME_OPEN = self.TIME_OPEN * mult

# [Go back to main.py, click here](./main.html)
