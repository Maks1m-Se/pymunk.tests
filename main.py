import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pymunk
import pymunk.pygame_util
import pymunk.constraints
import pygame

pygame.init()

display = pygame.display.set_mode((900, 800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, -900)
FPS = 50

def convert_coordinates(point):
    return int(point[0]), int(600-point[1])

class Ball():
    def __init__(self, x, y, size):
        self.body = pymunk.Body()
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, 10)
        self.size = size
        # reduce size range [10, 50] to density range [0.1, 1] 
        # out_min + (x - in_min) * (out_max - out_min) / (in_max - in_min)
        self.shape.density = 0.1 + (size - 10) * (1 - 0.1) / (50 - 10)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
    def draw(self):
        pygame.draw.circle(display, (255,0,0), convert_coordinates(self.body.position), self.size)

class String():
    def __init__(self, body1, attachment, identifier="body"):
        self.body1 = body1
        if identifier == "body":
            self.body2 = attachment
        elif identifier == "position":
            self.body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.body2.position = attachment
        joint = pymunk.PinJoint(self.body1, self.body2)
        space.add(joint)
    def draw(self):
        pos1 = convert_coordinates(self.body1.position)
        pos2 = convert_coordinates(self.body2.position)
        pygame.draw.line(display, (0,0,0), pos1, pos2, 2)


### GAME LOOP ###
def game():
    ball_1 = Ball(446, 472, 50) # x, y, size --> [between 10 and 50]
    ball_2 = Ball(442, 600, 20) # x, y, size --> [between 10 and 50]
    string_1 = String(ball_1.body, (450,300), "position")
    string_2 = String(ball_1.body, ball_2.body) # identifier automatically "body"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill((255, 255, 255))

        #draw objects
        ball_1.draw()
        ball_2.draw()
        string_1.draw()
        string_2.draw()

        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

game()
pygame.quit()

