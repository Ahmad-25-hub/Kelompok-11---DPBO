import pymunk

class Dinding:
    def __init__(self, space, poly_dims, elasticity=0.8):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (0, 0)
        shape = pymunk.Poly(body, poly_dims)
        shape.elasticity = elasticity
        space.add(body, shape)
        self.body = body
        self.shape = shape
