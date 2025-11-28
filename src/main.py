import pygame
import pymunk
import math
import sys

from objects.bola import Bola
from objects.meja import Meja
from objects.tongkat import Tongkat
from objects.dinding import Dinding
from renderer import draw_text, draw_projection_and_bounce
from game_manager import GameManager
from skor import Skor

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 678
BOTTOM_PANEL = 50

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + BOTTOM_PANEL))
pygame.display.set_caption("Pool Game")

space = pymunk.Space()
static_body = space.static_body

clock = pygame.time.Clock()
FPS = 120

# Game variables (preserve names & defaults from your latest main.py)
lives = 3
dia = 36
pocket_dia = 66
game_running = True
cue_ball_potted = False
taking_shot = True
potted_balls = []

# Aiming lock variables handled in manager
# Animation variables (same as updated main.py)
shot_animating = False
shot_offset = 0
final_force = 0
animation_speed = 40

# Colours & fonts
BG = (50, 50, 50)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

font = pygame.font.SysFont("Lato", 30)

# Load images (same error handling)
try:
    cue_image = pygame.image.load("src/assets/cue.png").convert_alpha()
    table_image = pygame.image.load("src/assets/table.png").convert_alpha()
    ball_images = []
    for i in range(1, 17):
        ball_image = pygame.image.load(f"src/assets/ball_{i}.png").convert_alpha()
        ball_images.append(ball_image)
except FileNotFoundError:
    print("Error: Gambar tidak ditemukan. Pastikan folder 'src/assets/' ada.")
    pygame.quit()
    sys.exit()

# Power bar
power_bar = pygame.Surface((10, 20))
power_bar.fill(RED)

# Objects & managers
meja = Meja(table_image)
tongkat = Tongkat(cue_image)
manager = GameManager()
score = Skor()

# Create balls (preserve original ordering)
balls = []
rows = 5
for col in range(5):
    for row in range(rows):
        pos = (250 + (col * (dia + 1)), 267 + (row * (dia + 1)) + (col * dia / 2))
        b = Bola(space, dia / 2, pos)
        balls.append(b)
    rows -= 1

# cue ball last (same pos)
cue_ball = Bola(space, dia / 2, (888, SCREEN_HEIGHT / 2))
balls.append(cue_ball)

# Pockets (tuple coords) and cushions (same geometry)
pockets = [
    (55, 63), (592, 48), (1134, 64),
    (55, 616), (592, 629), (1134, 616)
]

cushions = [
    [(88, 56), (109, 77), (555, 77), (564, 56)],
    [(621, 56), (630, 77), (1081, 77), (1102, 56)],
    [(89, 621), (110, 600), (556, 600), (564, 621)],
    [(622, 621), (630, 600), (1081, 600), (1102, 621)],
    [(56, 96), (77, 117), (77, 560), (56, 581)],
    [(1143, 96), (1122, 117), (1122, 560), (1143, 581)]
]

for c in cushions:
    Dinding(space, c)

run = True
while run:
    clock.tick(FPS)
    space.step(1 / FPS)

    screen.fill(BG)
    meja.draw(screen)

    # --- POTTING LOGIC (keputusan sama persis dengan file terbaru) ---
    for i, ball in enumerate(list(balls)):
        for pocket in pockets:
            ball_x_dist = abs(ball.body.position[0] - pocket[0])
            ball_y_dist = abs(ball.body.position[1] - pocket[1])
            ball_dist = math.sqrt((ball_x_dist ** 2) + (ball_y_dist ** 2))
            if ball_dist <= pocket_dia / 2:
                if i == len(balls) - 1:
                    lives -= 1
                    cue_ball_potted = True
                    ball.body.position = (-100, -100)
                    ball.body.velocity = (0.0, 0.0)
                else:
                    try:
                        space.remove(ball.body)
                        potted_balls.append(ball_images[i])
                        ball_images.pop(i)
                        balls.remove(ball)
                    except Exception:
                        pass

    # Draw pool balls
    for i, ball in enumerate(balls):
        if i < len(ball_images):
            screen.blit(ball_images[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

    # Check if all balls stopped
    taking_shot = True
    for ball in balls:
        if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
            taking_shot = False

    # STIK & TEMBAKAN
    if taking_shot and game_running:
        if cue_ball_potted:
            balls[-1].body.position = (888, SCREEN_HEIGHT / 2)
            cue_ball_potted = False

        mouse_pos = pygame.mouse.get_pos()

        # Aiming
        if not manager.aim_locked:
            x_dist = balls[-1].body.position[0] - mouse_pos[0]
            y_dist = -(balls[-1].body.position[1] - mouse_pos[1])
            cue_angle = math.degrees(math.atan2(y_dist, x_dist))
        else:
            cue_angle = manager.locked_angle

        tongkat.update(cue_angle)

        # Draw projection only if not animating (identical to latest main.py)
        if not shot_animating:
            draw_projection_and_bounce(screen, space, cue_angle, balls[-1], dia)

        # Powering up (visuals & calculations)
        if manager.powering_up and not shot_animating:
            drag_dist, visual_offset = manager.update_power(mouse_pos)
            force = manager.force
            shot_offset = min(drag_dist, 300)

            # Anchor visuals (same)
            pygame.draw.line(screen, YELLOW, manager.pull_start_pos, mouse_pos, 2)
            pygame.draw.circle(screen, YELLOW, manager.pull_start_pos, 5)
            pygame.draw.circle(screen, WHITE, mouse_pos, 3)

            # Power bar rendering (same scaling)
            for b in range(math.ceil(force / 2000) if force > 0 else 0):
                screen.blit(power_bar,
                            (balls[-1].body.position[0] - 30 + (b * 15),
                             balls[-1].body.position[1] + 30))

        # Shot animation handling (identical behaviour)
        elif shot_animating:
            # Stick moves forward fast (note: shot_offset was set when powering_up)
            shot_offset -= animation_speed
            if shot_offset <= 0:
                # Impact moment
                shot_offset = 0
                shot_animating = False

                ang = math.radians(manager.locked_angle)
                x_impulse = math.cos(ang)
                y_impulse = math.sin(ang)

                # apply stored force
                balls[-1].body.apply_impulse_at_local_point((final_force * -x_impulse, final_force * y_impulse), (0, 0))

                # reset lock & force like original
                manager.aim_locked = False
                force = 0

        # Draw stick using shot_offset (works for both pull and animation)
        tongkat.draw(screen, balls[-1].body.position, shot_offset)

    # UI
    draw_text(screen, f"LIVES: {lives}", font, WHITE, SCREEN_WIDTH - 200, SCREEN_HEIGHT + 10)

    # EVENTS (mouse down/up logic same as latest file)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and taking_shot:
            if not shot_animating:
                manager.mouse_down((balls[-1].body.position[0], balls[-1].body.position[1]), pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP and taking_shot:
            if manager.powering_up and manager.force > 0:
                # start animation: store final_force and set shot_animating True
                shot_animating = True
                final_force = manager.force
                # shot_offset is preserved from last visual pull (so stick will move forward)
            manager.mouse_up_start_animation()

    pygame.display.update()

pygame.quit()
