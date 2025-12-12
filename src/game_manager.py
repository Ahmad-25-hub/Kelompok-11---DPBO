import math
from config import *

def check_potted(balls, pockets, space, ball_images):
    # Mengembalikan list (bola yang dihapus, gambar bola tersebut) dan cue_ball_potted status
    potted_info = []
    cue_ball_potted = False

    for i, ball in enumerate(list(balls)):
        for pocket in pockets:
            ball_x_dist = abs(ball.body.position[0] - pocket[0])
            ball_y_dist = abs(ball.body.position[1] - pocket[1])
            ball_dist = math.sqrt((ball_x_dist ** 2) + (ball_y_dist ** 2))
            
            if ball_dist <= POCKET_DIA / 2:
                b_id = ball.ball_number

                if b_id == -1: # CUE BALL
                    cue_ball_potted = True
                    ball.body.position = (-100, -100)
                    ball.body.velocity = (0.0, 0.0)
                else:
                    try:
                        space.remove(ball.body)
                        balls.remove(ball)
                        # Ambil gambar bola yang sesuai (logic agak tricky karena index berubah)
                        # Kita asumsikan caller menangani index gambar
                        potted_info.append((ball, b_id, i)) 
                    except:
                        pass
    return potted_info, cue_ball_potted