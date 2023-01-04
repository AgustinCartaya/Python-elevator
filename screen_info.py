import pygame 
import os
from elevator import Elevator

# === Class used to monitor the current status of the elevator. ===

class ScreenInfo:
    def __init__(self, window):
        self.window = window

        self.selected_buttons = [0 for _ in range(8)]
        self.people_number = 0
        self.people_weight = 0
        self.current_floor = 0
        self.requested_floor = 0
        self.moving = 0
        self.current_state = ""
        self.emergency = False

        self.load_images()

    def refresh(self, info):
        # Refreshing information of the current floor
        self.current_floor = info["current_floor"]
        self.requested_floor = info["requested_floor"]

        # Refreshing state of the selected buttons
        selected_buttons = list(set(info["queue"]))
        self.selected_buttons = [0 for _ in range(8)]
        for i in selected_buttons:
            self.selected_buttons[i] = 1
        self.selected_buttons[self.requested_floor] = 1

        # Refreshing the number of people
        self.people_number = len(info["people"])

        # Refreshing the actual weight in the elevator.
        self.people_weight = info["people"].get_weight()

        # Refreshing state of the doors and direction of movement.
        self.current_state = info["current_state"]
        self.moving = info["moving"]

        self.emergency = info["emergency"]

    def load_images(self):
        #Loading of the necessary assets for the GUI.
        self.cp_size = (150, 350)
        self.cp_pos = (400, self.window.SCREEN_HEIGHT / 2 - self.cp_size[0])

        self.scren_pos = (self.cp_pos[0]+30, self.cp_pos[1]+30)
        self.arrow_size = (20, 20)

        self.i_button_size = (50, 50)
        self.i_button_pos = (self.cp_pos[0]+7, self.cp_pos[1]+50)


        self.img_control_panel =  pygame.image.load(os.path.join('src','img', "control_panel.png"))
        self.img_control_panel = pygame.transform.smoothscale(self.img_control_panel, self.cp_size)

        self.img_up =  pygame.image.load(os.path.join('src','img', "up.png"))
        self.img_up = pygame.transform.smoothscale(self.img_up, self.arrow_size)

        self.img_down =  pygame.image.load(os.path.join('src','img', "down.png"))
        self.img_down = pygame.transform.smoothscale(self.img_down, self.arrow_size)

        self.img_i_button =  pygame.image.load(os.path.join('src','img', "i_button.png"))
        self.img_i_button = pygame.transform.smoothscale(self.img_i_button, self.i_button_size)

        self.img_i_button_called =  pygame.image.load(os.path.join('src','img', "i_button_called.png"))
        self.img_i_button_called = pygame.transform.smoothscale(self.img_i_button_called, self.i_button_size)
        
        self.img_emergency_button =  pygame.image.load(os.path.join('src','img', "emergency_button.png"))
        self.img_emergency_button = pygame.transform.smoothscale(self.img_emergency_button, self.i_button_size)

        self.img_emergency_button_called =  pygame.image.load(os.path.join('src','img', "emergency_button_called.png"))
        self.img_emergency_button_called = pygame.transform.smoothscale(self.img_emergency_button_called, self.i_button_size)

    def draw(self):

        self.window.screen.blit(self.img_control_panel, self.cp_pos)


        # self.print_buttons
        font = pygame.font.SysFont(None, 24)
        
        # Drawing of the current floor.
        str_cfloor = 'Current floor %d ' % (7-self.current_floor)
        str_state = ""
        if self.current_state == Elevator.STATE_WATING:
            str_state = "X"
        elif self.current_state == Elevator.STATE_OPEN:
            str_state = "O"
        elif self.current_state == Elevator.STATE_MOVING:
            if self.moving > 0:
                str_state = "v"
                self.window.screen.blit(self.img_down, (self.scren_pos[0] + 48, self.scren_pos[1]+8))
            else:
                str_state = "^"
                self.window.screen.blit(self.img_up, (self.scren_pos[0] + 48, self.scren_pos[1]+8))
        
        # Current floor.
        font2 = pygame.font.SysFont(None, 36)
        img = font2.render(str(7-self.current_floor), True, (255,0,0))
        self.window.screen.blit(img, (self.scren_pos[0] + 28, self.scren_pos[1]+5))

        # Buttons.
        bt_number = 0
        bt_pos = (0, 0)
        for i in range(2):
            for j in range (4):
                bt_pos = (self.i_button_pos[0] + i * self.i_button_size[0] + 20, self.i_button_pos[1]+ j * self.i_button_size[1]+ 20)

                if self.selected_buttons[7-bt_number]==1:
                    self.window.screen.blit(self.img_i_button_called, bt_pos)
                else:
                    self.window.screen.blit(self.img_i_button, bt_pos)
                
                font2 = pygame.font.SysFont(None, 24)
                img = font2.render(str(bt_number), True, (30,30,30))
                self.window.screen.blit(img, (bt_pos[0]+21, bt_pos[1]+18))

                bt_number = bt_number +1
            
        if self.emergency:
            self.window.screen.blit(self.img_emergency_button_called, (bt_pos[0] - (self.i_button_size[0])/2, bt_pos[1] + self.i_button_size[1]/1.25))
        else:
            self.window.screen.blit(self.img_emergency_button, (bt_pos[0] - (self.i_button_size[0])/2, bt_pos[1] + self.i_button_size[1]/1.25))
        
        # Number of people.
        img = font.render('Number of people %d' % self.people_number, True, (0,0,0))
        self.window.screen.blit(img, (400, 20))

        # People weight.
        img = font.render('Actual weight %d' % self.people_weight, True, (0,0,0))
        self.window.screen.blit(img, (400, 40))

    def print_buttons(self):
        for i in range(self.selected_buttons):
            if self.selected_buttons[i] == 1:
                print("%d "%i)

# [Go back to main.py, click here](./main.html)
