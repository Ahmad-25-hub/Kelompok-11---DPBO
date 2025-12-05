import pygame
import pymunk
import math
import sys

# Import modul internal
from config import *
from physics import space, static_body
from renderer import *
from skor import draw_score_board
import game_manager as gm

# Import Objek
from objects.bola import create_ball, dia
from objects.meja import table_image
from objects.lubang import pockets, pocket_dia
from objects.tongkat import Cue
from objects.dinding import setup_cushions

# --- SETUP AWAL ---
# Init Cushion
setup_cushions(space)

# Setup Bola
balls = []
rows = 5
current_ball_num = 1 

for col in range(5):
    for row in range(rows):
        base_x = (250 * SCALE) + (col * (dia + (1 * SCALE)))
        base_y = (267 * SCALE) + (row * (dia + (1 * SCALE))) + (col * dia / 2)
        pos = (base_x + MARGIN_X, base_y + MARGIN_Y)
        new_ball = create_ball(space, dia / 2, pos)
        new_ball.ball_number = current_ball_num
        current_ball_num += 1
        balls.append(new_ball)
    rows -= 1

# Cue Ball
cue_ball_start_x = (888 * SCALE) + MARGIN_X
cue_ball_start_y = (TABLE_HEIGHT / 2) + MARGIN_Y
cue_ball_pos = (cue_ball_start_x, cue_ball_start_y)
cue_ball = create_ball(space, dia / 2, cue_ball_pos)
cue_ball.ball_number = -1 
balls.append(cue_ball)

# Init Cue
cue = Cue(balls[-1].body.position)
power_bar = pygame.Surface((10 * SCALE, 20 * SCALE))
power_bar.fill(RED)
animation_speed = 40 * SCALE 

# Callback Functions untuk Menu
def start_game_action():
    gm.game_state = "GAME"

def exit_game_action():
    global run
    run = False

# --- GAME LOOP ---
run = True
while run:
    clock.tick(FPS)
    
    # ==========================
    # LOGIKA MAIN MENU
    # ==========================
    if gm.game_state == "MENU":
        draw_main_menu(start_game_action, exit_game_action)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gm.game_state = "GAME"

    # ==========================
    # LOGIKA GAMEPLAY
    # ==========================
    elif gm.game_state == "GAME":
        space.step(1 / FPS)
        screen.fill(UI_BG)
        
        # Gambar Meja 
        screen.blit(table_image, (MARGIN_X, MARGIN_Y))

        # UI Scoreboard
        draw_score_board(gm.player1_group, gm.current_player, gm.potted_balls_1, gm.potted_balls_2)

        # Status Message
        if gm.shot_taken and not gm.game_over:
            status_text = font.render("WAITING FOR STOP...", True, GREY)
            screen.blit(status_text, (SCREEN_WIDTH/2 - status_text.get_width()/2, SCREEN_HEIGHT - (35 * SCALE)))

        # --- LOGIKA BOLA MASUK ---
        for i, ball in enumerate(list(balls)):
            for pocket in pockets:
                ball_x_dist = abs(ball.body.position[0] - pocket[0])
                ball_y_dist = abs(ball.body.position[1] - pocket[1])
                ball_dist = math.sqrt((ball_x_dist ** 2) + (ball_y_dist ** 2))
                
                if ball_dist <= pocket_dia / 2:
                    b_id = ball.ball_number

                    if b_id == -1: # CUE BALL
                        gm.cue_ball_potted = True
                        ball.body.position = (-100, -100)
                        ball.body.velocity = (0.0, 0.0)
                    else:
                        try:
                            space.remove(ball.body)
                            balls.remove(ball)
                            potted_img = ball_images[i] 
                            ball_images.pop(i) 
                            
                            if b_id == 8: # 8-BALL
                                my_balls_count = len(gm.potted_balls_1) if gm.current_player == 1 else len(gm.potted_balls_2)
                                if my_balls_count >= 7:
                                    gm.winner_text = f"PLAYER {gm.current_player} WINS!"
                                else:
                                    gm.winner_text = f"PLAYER {gm.current_player} LOSE! (8-Ball Early)"
                                gm.game_over = True
                                
                            else:
                                if gm.player1_group is None:
                                    is_solid = b_id < 8
                                    if gm.current_player == 1:
                                        gm.player1_group = "solids" if is_solid else "stripes"
                                    else:
                                        gm.player1_group = "stripes" if is_solid else "solids"

                            if gm.current_player == 1:
                                gm.potted_balls_1.append(potted_img)
                            else:
                                gm.potted_balls_2.append(potted_img)
                                
                            gm.potted_this_turn = True 
                        except Exception as e:
                            pass

        # Draw pool balls
        for i, ball in enumerate(balls):
            if ball.ball_number == -1:
                pygame.draw.circle(screen, WHITE, (int(ball.body.position[0]), int(ball.body.position[1])), int(dia/2))
            elif i < len(ball_images):
                screen.blit(ball_images[i], (ball.body.position[0] - (dia/2), ball.body.position[1] - (dia/2)))

        # Check stopped
        gm.taking_shot = True
        for ball in balls:
            if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
                gm.taking_shot = False

        # Turn System Logic
        if gm.taking_shot == True and gm.shot_taken == True and not gm.game_over:
            gm.shot_taken = False 
            if gm.cue_ball_potted:
                balls[-1].body.position = (cue_ball_start_x, cue_ball_start_y)
                balls[-1].body.velocity = (0, 0)
                gm.cue_ball_potted = False
                gm.current_player = 2 if gm.current_player == 1 else 1
            elif gm.potted_this_turn:
                pass 
            else:
                gm.current_player = 2 if gm.current_player == 1 else 1
            gm.potted_this_turn = False

        # --- INPUT HANDLER ---
        if not gm.game_over:
            if gm.taking_shot == True:
                if gm.cue_ball_potted == True:
                    balls[-1].body.position = (cue_ball_start_x, cue_ball_start_y)
                    gm.cue_ball_potted = False

                mouse_pos = pygame.mouse.get_pos()

                if not gm.aim_locked:
                    x_dist = balls[-1].body.position[0] - mouse_pos[0]
                    y_dist = -(balls[-1].body.position[1] - mouse_pos[1])
                    gm.cue_angle = math.degrees(math.atan2(y_dist, x_dist))
                else:
                    gm.cue_angle = gm.locked_angle

                cue.update(gm.cue_angle)

                # Draw Aim Line 
                if not gm.shot_animating: 
                    angle_rad = math.radians(gm.cue_angle)
                    proj_vec_x = -math.cos(angle_rad)
                    proj_vec_y = math.sin(angle_rad)
                    start_pt = balls[-1].body.position
                    offset_dist = (dia / 2) + 2 
                    ray_start = (start_pt[0] + proj_vec_x * offset_dist, start_pt[1] + proj_vec_y * offset_dist)
                    ray_end = (start_pt[0] + proj_vec_x * (1500 * SCALE), start_pt[1] + proj_vec_y * (1500 * SCALE))
                    
                    query = space.segment_query_first(ray_start, ray_end, 1, pymunk.ShapeFilter())
                    if query:
                        end_point = query.point
                        pygame.draw.line(screen, WHITE, start_pt, end_point, 2)
                        pygame.draw.circle(screen, WHITE, (int(end_point[0]), int(end_point[1])), 4)
                        
                        if hasattr(query, 'normal'):
                            normal_x = query.normal.x
                            normal_y = query.normal.y
                            bounce_vec_x, bounce_vec_y = 0, 0
                            line_color = WHITE
                            if hasattr(query.shape.body, 'body_type') and query.shape.body.body_type == pymunk.Body.STATIC:
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
                                line_color = (255, 255, 0)
                            bounce_start = (end_point[0] + bounce_vec_x * 2, end_point[1] + bounce_vec_y * 2)
                            bounce_len = 200 * SCALE
                            bounce_end = (bounce_start[0] + bounce_vec_x * bounce_len, bounce_start[1] + bounce_vec_y * bounce_len)
                            pygame.draw.line(screen, line_color, end_point, bounce_end, 2)
                    else:
                        pygame.draw.line(screen, WHITE, start_pt, ray_end, 2)

                # Power Logic
                if gm.powering_up == True and not gm.shot_animating:
                    drag_x_dist = mouse_pos[0] - gm.pull_start_pos[0]
                    drag_y_dist = mouse_pos[1] - gm.pull_start_pos[1]
                    drag_dist = math.sqrt(drag_x_dist**2 + drag_y_dist**2)
                    
                    new_sensitivity = 35 * SCALE 
                    gm.force = drag_dist * new_sensitivity
                    max_f = gm.max_force * SCALE
                    if gm.force > max_f: gm.force = max_f
                    gm.shot_offset = min(drag_dist, 300 * SCALE) 

                    pygame.draw.line(screen, YELLOW, gm.pull_start_pos, mouse_pos, 2)
                    pygame.draw.circle(screen, YELLOW, gm.pull_start_pos, 5)
                    pygame.draw.circle(screen, WHITE, mouse_pos, 3)

                    bar_step = 2000 * SCALE
                    num_bars = math.ceil(gm.force / bar_step) if gm.force > 0 and bar_step > 0 else 0
                    for b in range(num_bars):
                        screen.blit(power_bar,
                        (balls[-1].body.position[0] - (30 * SCALE) + (b * (15 * SCALE)),
                        balls[-1].body.position[1] + (30 * SCALE)))
                
                elif gm.shot_animating == True:
                    gm.shot_offset -= animation_speed 
                    if gm.shot_offset <= 0:
                        gm.shot_offset = 0
                        gm.shot_animating = False
                        x_impulse = math.cos(math.radians(gm.locked_angle))
                        y_impulse = math.sin(math.radians(gm.locked_angle))
                        balls[-1].body.apply_impulse_at_local_point((gm.final_force * -x_impulse, gm.final_force * y_impulse), (0, 0))
                        gm.aim_locked = False
                        gm.force = 0
                        gm.shot_taken = True
                        gm.potted_this_turn = False
                
                cue.draw(screen, balls[-1].body.position, gm.shot_offset)
        
        # --- GAME OVER SCREEN ---
        else:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BG)
            screen.blit(overlay, (0,0))
            draw_centered_text("GAME OVER", large_font, WHITE, -50)
            draw_centered_text(gm.winner_text, large_font, GREEN, 20)
            draw_centered_text("Close and Restart to Play Again", font, YELLOW, 80)

        # --- EVENT HANDLER GAMEPLAY ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not gm.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and gm.taking_shot == True:
                    if not gm.shot_animating:
                        gm.powering_up = True
                        gm.pull_start_pos = pygame.mouse.get_pos()
                        gm.force = 0
                        mouse_x, mouse_y = gm.pull_start_pos
                        x_dist = balls[-1].body.position[0] - mouse_x
                        y_dist = -(balls[-1].body.position[1] - mouse_y)
                        gm.locked_angle = math.degrees(math.atan2(y_dist, x_dist))
                        gm.aim_locked = True

                if event.type == pygame.MOUSEBUTTONUP and gm.taking_shot == True:
                    if gm.powering_up and gm.force > 0:
                        gm.shot_animating = True   
                        gm.final_force = gm.force     
                    gm.powering_up = False

    pygame.display.update()

pygame.quit()