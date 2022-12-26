from people_group import PeopleGroup
from person import Person
import random
import threading
import pygame 
import os
# this class model a floor
class Floor:
    lock = threading.Lock()

    # time (in seconds) to show the people that went out from the elevator 
    TIME_PEOPLE_OUT = 2

    # max number of random people that can be created by each request of the main
    MAX_RANDOM_PEOPLE = 5

    EMERGENCY_POSSIBILITY = 100

    def __init__(self, window, number):
        self.window = window
        self.number = number

        self.people_pos = (260, 65 + self.number*94)
        self.door_pos = (220, 40 + self.number*94)
        
        self.door_size = (80, 85)
        self.button_size = (20, 20)
        self.people = PeopleGroup([])

        self.people_out = PeopleGroup([])
        self.time_out_counter = 0

        self.called = False
        self.open = False

        self.load_images()
        # self.create_people()

    # create from 0 up to MAX_RANDOM_PEOPLE people ramdomly and add to the people group
    # the people is create only if there is not people on the floor, otherwise no body is created
    def create_people(self):
        self.lock.acquire()
        if len(self.people) == 0:
            nb_people = random.randint(0,3)
            emergency_chance = random.randint(0,self.EMERGENCY_POSSIBILITY) == 1
            for i in range(nb_people):
                person = Person(self.number, random.randint(0,7),  weight=random.randint(45,130), gender=bool(random.getrandbits(1)) )
                if emergency_chance:
                    person.exit_floor = -1
                # person = Person(self.number, self.number,  weight=random.randint(45,90), gender=bool(random.getrandbits(1)) )
                self.people.add_person(person)
        self.lock.release()

    # function called when the elevator is called on this floor
    def call_elevator(self, elevator):
        elevator.external_request(self.number)
        self.called = True


    # open the door of the floor 
    # people_going_out: contain the people going out from the elevator
    # return the people that wants to enter in the elevator
    # lock is required for the modification of the people on the floor
    # (to no create and remove at the same tima)
    def open_door(self, people_going_out):
        self.lock.acquire()

        self.people_out = people_going_out
        self.time_out_counter = self.TIME_PEOPLE_OUT

        enter = self.people.people
        self.people.remove_all()

        self.open = True 
        self.called = False
        self.lock.release()
        return PeopleGroup(enter)

    # take back the people that canno enter insithe the elevator (because is full)
    def over_weight(self, people):
        self.lock.acquire()
        self.people.join(people)
        self.lock.release()

    # close the door of the floor
    def close_door(self):
        self.open = False

    # remove the people that went out of the elevator
    def clear_people_out(self):
        if self.time_out_counter > 0:
            self.time_out_counter = self.time_out_counter - 1/self.window.FPS
        else:
            self.people_out = PeopleGroup([])

    def load_images(self):
        self.img_door_open =  pygame.image.load(os.path.join('src','img', "door_open.png"))
        self.img_door_open = pygame.transform.smoothscale(self.img_door_open, self.door_size)

        self.img_door_closed =  pygame.image.load(os.path.join('src','img', "door_closed.png"))
        self.img_door_closed = pygame.transform.smoothscale(self.img_door_closed, self.door_size)

        self.img_button = pygame.image.load(os.path.join('src','img', "button.png"))
        self.img_button = pygame.transform.smoothscale(self.img_button, self.button_size)

        self.img_button_called = pygame.image.load(os.path.join('src','img', "button_called.png"))
        self.img_button_called = pygame.transform.smoothscale(self.img_button_called, self.button_size)

    # draw the floor
    # also draw the people on the floor
    def draw(self):
        # draw door
        if self.open:
            self.window.screen.blit(self.img_door_open, self.door_pos)
        else:
            self.window.screen.blit(self.img_door_closed, self.door_pos)


        # draw call button
        if self.called:
            self.window.screen.blit(self.img_button_called, (self.door_pos[0] + self.door_size[0]-self.button_size[0], self.door_pos[1]+ self.door_size[1]/2 -self.button_size[1]/2))
        else:
            self.window.screen.blit(self.img_button, (self.door_pos[0] + self.door_size[0]-self.button_size[0], self.door_pos[1]+ self.door_size[1]/2 -self.button_size[1]/2))


        # draw people
        p_i = 0
        p_space = 25
        for p in self.people:
            self.window.screen.blit(p.img, (self.people_pos[0]-p_i*p_space, self.people_pos[1]))
            p_i = p_i + 1

        p_i = 0    
        for p in self.people_out:
            self.window.screen.blit(p.img, (50 + p_i*p_space, self.people_pos[1]))
            p_i = p_i + 1

    

        self.clear_people_out()

    # return True if the floor has people queuing for the elevator
    def has_people(self):
        return len(self.people) > 0

    def acceleration(self, mult):
        self.TIME_PEOPLE_OUT = self.TIME_PEOPLE_OUT * mult

