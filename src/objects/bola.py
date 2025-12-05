import pymunk
from config import *

# Ukuran bola
dia = int(36 * SCALE)

def create_ball(space, radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 5
    shape.elasticity = 0.8
    pivot = pymunk.PivotJoint(space.static_body, body, (0, 0), (0, 0))
    pivot.max_bias = 0
    pivot.max_force = 1000 
    space.add(body, shape, pivot)
    return shape