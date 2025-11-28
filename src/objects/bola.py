import pymunk
from .objek_game import ObjekGame

class Bola(ObjekGame):
    def __init__(self, space, radius, pos):
        self.space = space
        self.radius = radius

        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Circle(body, radius)

        shape.mass = 5
        shape.elasticity = 0.8

        pivot = pymunk.PivotJoint(space.static_body, body, (0, 0), (0, 0))
        pivot.max_bias = 0
        pivot.max_force = 1000

        space.add(body, shape, pivot)

        self.body = body
        self.shape = shape

    def draw(self, surface, img):
        x = int(self.body.position.x - self.radius)
        y = int(self.body.position.y - self.radius)
        surface.blit(img, (x, y))
