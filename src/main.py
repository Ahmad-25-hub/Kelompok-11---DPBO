import pygame
import pymunk
import pymunk.pygame_util
import math

# --- IMPORTS MODULE SENDIRI ---
import config as conf
import physics as phys
import renderer as renderer
import skor as skor 
import game_manager as gm

from objects.bola import create_ball
from objects.dinding import init_cushions
from objects.lubang import get_pockets
from objects.meja import load_table_image
from objects.tongkat import Cue
from objects.objek_game import load_ball_images

# --- INISIALISASI ---
pygame.init()
conf.init_fonts() # Inisialisasi font setelah pygame.init

screen = pygame.display.set_mode((conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT))
pygame.display.set_caption("Pool Game - Single & Multiplayer")

clock = pygame.time.Clock()

# --- GAME VARIABLES ---
game_state = "MENU"
game_mode = "MULTI"
force = 0
max_force = 10000 * conf.SCALE
force_direction = 1
game_running = True
cue_ball_potted = False
taking_shot = True
powering_up = False
pull_start_pos = (0, 0)
aim_locked = False
locked_angle = 0
cue_angle = 0
shot_animating = False     
shot_offset = 0            
final_force = 0            
animation_speed = 40 * conf.SCALE 

current_player = 1         
potted_this_turn = False   
shot_taken = False         
potted_balls_1 = [] 
potted_balls_2 = [] 
game_over = False
winner_text = ""
player1_group = None

# --- LOAD ASSETS ---
try:
    menu_bg_orig = pygame.image.load("assets/background_main_menu.png").convert()
    menu_bg = pygame.transform.scale(menu_bg_orig, (conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT))
except:
    menu_bg = pygame.Surface((conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT))
    menu_bg.fill(conf.BG)

cue_image_orig = pygame.image.load("assets/images/cue.png").convert_alpha()
cue_w = cue_image_orig.get_width() * conf.SCALE
cue_h = cue_image_orig.get_height() * conf.SCALE
cue_image = pygame.transform.scale(cue_image_orig, (int(cue_w), int(cue_h)))

table_image = load_table_image()
ball_images = load_ball_images()

# --- INIT OBJECTS ---
init_cushions() # Buat dinding meja
pockets = get_pockets()

balls = []
rows = 5
current_ball_num = 1 

# Setup Bola Pool
for col in range(5):
    for row in range(rows):
        base_x = (250 * conf.SCALE) + (col * (conf.DIA + (1 * conf.SCALE)))
        base_y = (267 * conf.SCALE) + (row * (conf.DIA + (1 * conf.SCALE))) + (col * conf.DIA / 2)
        pos = (base_x + conf.MARGIN_X, base_y + conf.MARGIN_Y)
        new_ball = create_ball(conf.DIA / 2, pos, current_ball_num)
        current_ball_num += 1
        balls.append(new_ball)
    rows -= 1

# Setup Cue Ball
cue_ball_start_x = (888 * conf.SCALE) + conf.MARGIN_X
cue_ball_start_y = (conf.TABLE_HEIGHT / 2) + conf.MARGIN_Y
cue_ball_pos = (cue_ball_start_x, cue_ball_start_y)
cue_ball = create_ball(conf.DIA / 2, cue_ball_pos, -1)
balls.append(cue_ball)

cue = Cue(balls[-1].body.position, cue_image)
power_bar = pygame.Surface((10 * conf.SCALE, 20 * conf.SCALE))
power_bar.fill(conf.RED)

# --- INIT TOMBOL MENU ---
button_width = 300 * conf.SCALE
button_height = 70 * conf.SCALE
center_x = (conf.SCREEN_WIDTH // 2) - (button_width // 2)
start_y = (conf.SCREEN_HEIGHT // 2) - (40 * conf.SCALE)

btn_1_player = renderer.Button(center_x, start_y, button_width, button_height, "1 PLAYER", conf.large_font)
btn_2_player = renderer.Button(center_x, start_y + button_height + (20 * conf.SCALE), button_width, button_height, "2 PLAYERS", conf.large_font)
exit_button = renderer.Button(center_x, start_y + (button_height * 2) + (40 * conf.SCALE), button_width, button_height, "EXIT", conf.large_font)


def draw_main_menu():
    global game_state, run, game_mode
    screen.blit(menu_bg, (0, 0))
    overlay = pygame.Surface((conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT))
    overlay.set_alpha(100)
    overlay.fill(conf.BLACK)
    screen.blit(overlay, (0,0))

    title_text = "BILLIARD MASTER"
    title_surf = conf.title_font.render(title_text, True, conf.WHITE)
    shadow_surf = conf.title_font.render(title_text, True, conf.BLACK)
    title_rect = title_surf.get_rect(center=(conf.SCREEN_WIDTH//2, conf.SCREEN_HEIGHT//2 - (180 * conf.SCALE)))
    screen.blit(shadow_surf, (title_rect.x + 4, title_rect.y + 4))
    screen.blit(title_surf, title_rect)

    if btn_1_player.draw(screen):
        game_mode = "SINGLE"
        game_state = "GAME"
    if btn_2_player.draw(screen):
        game_mode = "MULTI"
        game_state = "GAME"
    if exit_button.draw(screen):
        run = False
    
    renderer.draw_centered_text(screen, "Select Game Mode", conf.small_font, conf.GREY, y_offset=(320 * conf.SCALE))

# --- MAIN LOOP ---
run = True
while run:
    clock.tick(conf.FPS)
    
    if game_state == "MENU":
        draw_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_mode = "SINGLE"
                    game_state = "GAME"
                if event.key == pygame.K_2:
                    game_mode = "MULTI"
                    game_state = "GAME"

    elif game_state == "GAME":
        phys.space.step(1 / conf.FPS)
        screen.fill(conf.UI_BG)
        screen.blit(table_image, (conf.MARGIN_X, conf.MARGIN_Y))

        skor.draw_score_board(screen, game_mode, current_player, potted_balls_1, potted_balls_2, player1_group)

        if shot_taken and not game_over:
            status_text = conf.font.render("WAITING FOR STOP...", True, conf.GREY)
            screen.blit(status_text, (conf.SCREEN_WIDTH/2 - status_text.get_width()/2, conf.SCREEN_HEIGHT - (35 * conf.SCALE)))

        # LOGIKA BOLA MASUK (Manual implementation in loop to access globals easily)
        # Note: Logic extracted partially to game_manager but lists are here
        for i, ball in enumerate(list(balls)):
            for pocket in pockets:
                ball_x_dist = abs(ball.body.position[0] - pocket[0])
                ball_y_dist = abs(ball.body.position[1] - pocket[1])
                ball_dist = math.sqrt((ball_x_dist ** 2) + (ball_y_dist ** 2))
                
                if ball_dist <= conf.POCKET_DIA / 2:
                    b_id = ball.ball_number
                    if b_id == -1:
                        cue_ball_potted = True
                        ball.body.position = (-100, -100)
                        ball.body.velocity = (0.0, 0.0)
                    else:
                        try:
                            phys.space.remove(ball.body)
                            balls.remove(ball)
                            
                            # Handle images list sync
                            # Find index in original images list based on ball sequence is hard
                            # Simplified: We pop from ball_images same index as ball in balls list if synced
                            # But wait, 'i' is iterating current balls. 
                            # We need to map ball number to image.
                            # Original code just popped i. Let's do that but careful.
                            potted_img = ball_images[i] 
                            ball_images.pop(i) 

                            if b_id == 8:
                                if game_mode == "SINGLE":
                                    if len(potted_balls_1) >= 14:
                                        winner_text = "YOU WIN! (Table Cleared)"
                                    else:
                                        winner_text = "GAME OVER! (8-Ball Early)"
                                    game_over = True
                                else:
                                    my_balls_count = len(potted_balls_1) if current_player == 1 else len(potted_balls_2)
                                    if my_balls_count >= 7:
                                        winner_text = f"PLAYER {current_player} WINS!"
                                    else:
                                        winner_text = f"PLAYER {current_player} LOSE! (8-Ball Early)"
                                    game_over = True
                            else:
                                if game_mode == "MULTI" and player1_group is None:
                                    is_solid = b_id < 8
                                    if current_player == 1:
                                        player1_group = "solids" if is_solid else "stripes"
                                    else:
                                        player1_group = "stripes" if is_solid else "solids"

                            if game_mode == "SINGLE":
                                potted_balls_1.append(potted_img)
                            else:
                                if current_player == 1:
                                    potted_balls_1.append(potted_img)
                                else:
                                    potted_balls_2.append(potted_img)
                            potted_this_turn = True 
                        except:
                            pass

        # Draw balls
        for i, ball in enumerate(balls):
            if ball.ball_number == -1:
                pygame.draw.circle(screen, conf.WHITE, (int(ball.body.position[0]), int(ball.body.position[1])), int(conf.DIA/2))
            elif i < len(ball_images):
                screen.blit(ball_images[i], (ball.body.position[0] - (conf.DIA/2), ball.body.position[1] - (conf.DIA/2)))

        # Check stopped
        taking_shot = True
        for ball in balls:
            if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
                taking_shot = False

        # Turn System
        if taking_shot == True and shot_taken == True and not game_over:
            shot_taken = False 
            if cue_ball_potted:
                balls[-1].body.position = (cue_ball_start_x, cue_ball_start_y)
                balls[-1].body.velocity = (0, 0)
                cue_ball_potted = False
                if game_mode == "MULTI":
                    current_player = 2 if current_player == 1 else 1
            elif potted_this_turn:
                pass 
            else:
                if game_mode == "MULTI":
                    current_player = 2 if current_player == 1 else 1
            potted_this_turn = False

        # Input Handler
        if not game_over:
            if taking_shot == True and game_running == True:
                if cue_ball_potted == True:
                    balls[-1].body.position = (cue_ball_start_x, cue_ball_start_y)
                    cue_ball_potted = False

                mouse_pos = pygame.mouse.get_pos()

                if not aim_locked:
                    x_dist = balls[-1].body.position[0] - mouse_pos[0]
                    y_dist = -(balls[-1].body.position[1] - mouse_pos[1])
                    cue_angle = math.degrees(math.atan2(y_dist, x_dist))
                else:
                    cue_angle = locked_angle

                cue.update(cue_angle)

                # Draw Aim Line (Logic kept inline for simplicity with physics raycast)
                if not shot_animating: 
                    angle_rad = math.radians(cue_angle)
                    proj_vec_x = -math.cos(angle_rad)
                    proj_vec_y = math.sin(angle_rad)
                    start_pt = balls[-1].body.position
                    offset_dist = (conf.DIA / 2) + 2 
                    ray_start = (start_pt[0] + proj_vec_x * offset_dist, start_pt[1] + proj_vec_y * offset_dist)
                    ray_end = (start_pt[0] + proj_vec_x * (1500 * conf.SCALE), start_pt[1] + proj_vec_y * (1500 * conf.SCALE))
                    
                    query = phys.space.segment_query_first(ray_start, ray_end, 1, pymunk.ShapeFilter())
                    if query:
                        end_point = query.point
                        pygame.draw.line(screen, conf.WHITE, start_pt, end_point, 2)
                        pygame.draw.circle(screen, conf.WHITE, (int(end_point[0]), int(end_point[1])), 4)
                        
                        if hasattr(query, 'normal'):
                            normal_x = query.normal.x
                            normal_y = query.normal.y
                            bounce_vec_x, bounce_vec_y = 0, 0
                            line_color = conf.WHITE
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
                            bounce_len = 200 * conf.SCALE
                            bounce_end = (bounce_start[0] + bounce_vec_x * bounce_len, bounce_start[1] + bounce_vec_y * bounce_len)
                            pygame.draw.line(screen, line_color, end_point, bounce_end, 2)
                    else:
                        pygame.draw.line(screen, conf.WHITE, start_pt, ray_end, 2)

                # Power Logic
                if powering_up == True and not shot_animating:
                    drag_x_dist = mouse_pos[0] - pull_start_pos[0]
                    drag_y_dist = mouse_pos[1] - pull_start_pos[1]
                    drag_dist = math.sqrt(drag_x_dist**2 + drag_y_dist**2)
                    
                    new_sensitivity = 35 * conf.SCALE 
                    force = drag_dist * new_sensitivity
                    if force > max_force: force = max_force
                    shot_offset = min(drag_dist, 300 * conf.SCALE) 

                    pygame.draw.line(screen, conf.YELLOW, pull_start_pos, mouse_pos, 2)
                    pygame.draw.circle(screen, conf.YELLOW, pull_start_pos, 5)
                    pygame.draw.circle(screen, conf.WHITE, mouse_pos, 3)

                    bar_step = 2000 * conf.SCALE
                    num_bars = math.ceil(force / bar_step) if force > 0 and bar_step > 0 else 0
                    for b in range(num_bars):
                        screen.blit(power_bar,
                        (balls[-1].body.position[0] - (30 * conf.SCALE) + (b * (15 * conf.SCALE)),
                        balls[-1].body.position[1] + (30 * conf.SCALE)))
                
                elif shot_animating == True:
                    shot_offset -= animation_speed 
                    if shot_offset <= 0:
                        shot_offset = 0
                        shot_animating = False
                        x_impulse = math.cos(math.radians(locked_angle))
                        y_impulse = math.sin(math.radians(locked_angle))
                        balls[-1].body.apply_impulse_at_local_point((final_force * -x_impulse, final_force * y_impulse), (0, 0))
                        aim_locked = False
                        force = 0
                        shot_taken = True
                        potted_this_turn = False
                
                cue.draw(screen, balls[-1].body.position, shot_offset)
        
        else: # GAME OVER SCREEN
            overlay = pygame.Surface((conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(conf.BG)
            screen.blit(overlay, (0,0))
            renderer.draw_centered_text(screen, "GAME OVER", conf.large_font, conf.WHITE, -50)
            renderer.draw_centered_text(screen, winner_text, conf.large_font, conf.GREEN, 20)
            renderer.draw_centered_text(screen, "Close and Restart to Play Again", conf.font, conf.YELLOW, 80)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and taking_shot == True:
                    if not shot_animating:
                        powering_up = True
                        pull_start_pos = pygame.mouse.get_pos()
                        force = 0
                        mouse_x, mouse_y = pull_start_pos
                        x_dist = balls[-1].body.position[0] - mouse_x
                        y_dist = -(balls[-1].body.position[1] - mouse_y)
                        locked_angle = math.degrees(math.atan2(y_dist, x_dist))
                        aim_locked = True

                if event.type == pygame.MOUSEBUTTONUP and taking_shot == True:
                    if powering_up and force > 0:
                        shot_animating = True   
                        final_force = force     
                    powering_up = False

    pygame.display.update()

pygame.quit()