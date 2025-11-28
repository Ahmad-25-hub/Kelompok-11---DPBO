import math
import pygame
import pymunk

WHITE = (255,255,255)
YELLOW = (255,255,0)

def draw_text(surface, text, font, color, x, y):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

def draw_projection_and_bounce(screen, space, cue_angle, cue_ball, dia):
    """
    Menggambar proyeksi garis tembakan + satu pantulan sesuai algoritme di main.py (file terbaru).
    """
    angle_rad = math.radians(cue_angle)
    proj_vec_x = -math.cos(angle_rad)
    proj_vec_y = math.sin(angle_rad)

    start_pt = (cue_ball.body.position.x, cue_ball.body.position.y)
    offset_dist = (dia / 2) + 2
    ray_start = (start_pt[0] + proj_vec_x * offset_dist, start_pt[1] + proj_vec_y * offset_dist)
    ray_end = (start_pt[0] + proj_vec_x * 1200, start_pt[1] + proj_vec_y * 1200)

    query = space.segment_query_first(ray_start, ray_end, 1, pymunk.ShapeFilter())

    if query:
        end_point = query.point
        pygame.draw.line(screen, WHITE, start_pt, end_point, 2)
        pygame.draw.circle(screen, WHITE, (int(end_point[0]), int(end_point[1])), 4)

        hit_shape = query.shape
        normal_x = query.normal.x
        normal_y = query.normal.y

        bounce_vec_x, bounce_vec_y = 0, 0
        line_color = WHITE

        if hit_shape.body.body_type == pymunk.Body.STATIC:
            dot_product = (proj_vec_x * normal_x) + (proj_vec_y * normal_y)
            bounce_vec_x = proj_vec_x - (2 * dot_product * normal_x)
            bounce_vec_y = proj_vec_y - (2 * dot_product * normal_y)
            line_color = (200, 200, 200)
        else:
            tangent_x_1, tangent_y_1 = -normal_y, normal_x
            tangent_x_2, tangent_y_2 = normal_y, -normal_x
            dot_product_1 = (proj_vec_x * tangent_x_1) + (proj_vec_y * tangent_y_1)
            if dot_product_1 > 0:
                bounce_vec_x, bounce_vec_y = tangent_x_1, tangent_y_1
            else:
                bounce_vec_x, bounce_vec_y = tangent_x_2, tangent_y_2
            line_color = YELLOW

        bounce_start = (end_point[0] + bounce_vec_x * 2, end_point[1] + bounce_vec_y * 2)
        bounce_len = 200
        bounce_end = (bounce_start[0] + bounce_vec_x * bounce_len, bounce_start[1] + bounce_vec_y * bounce_len)
        pygame.draw.line(screen, line_color, end_point, bounce_end, 2)
    else:
        pygame.draw.line(screen, WHITE, start_pt, ray_end, 2)
