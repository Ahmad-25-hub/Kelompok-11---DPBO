import pymunk

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

def create_cushion(space, poly_dims, elasticity=0.8):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (0, 0)
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = elasticity
    space.add(body, shape)
    return shape
