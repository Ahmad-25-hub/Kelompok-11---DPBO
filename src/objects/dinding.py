import pymunk
from config import *

raw_cushions_orig = [
    [(88, 56), (109, 77), (555, 77), (564, 56)],
    [(621, 56), (630, 77), (1081, 77), (1102, 56)],
    [(89, 621), (110, 600), (556, 600), (564, 621)],
    [(622, 621), (630, 600), (1081, 600), (1102, 621)],
    [(56, 96), (77, 117), (77, 560), (56, 581)],
    [(1143, 96), (1122, 117), (1122, 560), (1143, 581)]
]

def create_cushion(space, poly_dims):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = ((0, 0))
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = 0.8
    space.add(body, shape)

def setup_cushions(space):
    for c_poly in raw_cushions_orig:
        scaled_poly = []
        for point in c_poly:
            sx = (point[0] * SCALE) + MARGIN_X
            sy = (point[1] * SCALE) + MARGIN_Y
            scaled_poly.append((sx, sy))
        create_cushion(space, scaled_poly)