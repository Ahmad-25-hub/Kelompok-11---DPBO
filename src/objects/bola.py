import pygame
import pymunk
from config import *
from physics import space, static_body

def create_ball(radius, pos, number):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 5
    shape.elasticity = 0.8
    
    # Pivot joint untuk simulasi gesekan meja
    pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
    pivot.max_bias = 0
    pivot.max_force = 1000 
    
    space.add(body, shape, pivot)
    
    # Simpan atribut custom
    shape.ball_number = number
    return shape