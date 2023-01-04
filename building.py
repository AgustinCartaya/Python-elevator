import pygame
import os

# === Class that models the building===
class Building:
    IMG_NAME = 'building.png'
    def __init__(self, window):
        self.window = window
        self.img = ""

        self.load_image()
# Just asset configuration.
    def load_image(self):
        self.img = pygame.image.load(os.path.join('src','img', self.IMG_NAME))
        self.img = pygame.transform.smoothscale(self.img,(300, self.window.SCREEN_HEIGHT))

    def draw(self):
        self.window.screen.blit(self.img, (0,0))

# [Go back to main.py, click here](./main.html)
