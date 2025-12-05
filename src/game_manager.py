# Game State Management
game_state = "MENU"
current_player = 1
player1_group = None
game_over = False
winner_text = ""
taking_shot = True
shot_taken = False
potted_this_turn = False
cue_ball_potted = False
potted_balls_1 = []
potted_balls_2 = []

# Physics & Input vars
force = 0
max_force = 10000 # akan dikalikan scale nanti
force_direction = 1
powering_up = False
pull_start_pos = (0, 0)
aim_locked = False
locked_angle = 0
cue_angle = 0
shot_animating = False     
shot_offset = 0            
final_force = 0