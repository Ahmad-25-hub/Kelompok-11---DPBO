import pygame
from config import *
from renderer import draw_text

def draw_score_board(screen, game_mode, current_player, potted_balls_1, potted_balls_2, player1_group):
    header_height = MARGIN_Y - (20 * SCALE)
    pygame.draw.rect(screen, PANEL_BG, (0, 0, SCREEN_WIDTH, header_height))
    pygame.draw.line(screen, WHITE, (0, header_height), (SCREEN_WIDTH, header_height), 2)

    # --- TAMPILAN SINGLE PLAYER ---
    if game_mode == "SINGLE":
        panel_rect = pygame.Rect(20 * SCALE, 10 * SCALE, SCREEN_WIDTH - (40 * SCALE), header_height - (20 * SCALE))
        pygame.draw.rect(screen, UI_BG, panel_rect, border_radius=10)
        pygame.draw.rect(screen, ACTIVE_BORDER, panel_rect, 2, border_radius=10)

        import config as conf
        draw_text(screen, f"SOLO PRACTICE MODE", conf.font, YELLOW, panel_rect.x + 20, panel_rect.y + 10)
        
        potted_count = len(potted_balls_1)
        remaining = 15 - potted_count
        status_info = f"Potted: {potted_count} | Remaining: {remaining}"
        
        status_surf = conf.font.render(status_info, True, WHITE)
        screen.blit(status_surf, (panel_rect.right - status_surf.get_width() - 20, panel_rect.y + 10))

        ball_start_x = panel_rect.x + 20
        ball_start_y = panel_rect.y + 45 * SCALE
        for i, ball_img in enumerate(potted_balls_1):
            screen.blit(ball_img, (ball_start_x + (i * (35 * SCALE)), ball_start_y))

    # --- TAMPILAN MULTIPLAYER ---
    else:
        p1_type = "SOLIDS" if player1_group == "solids" else ("STRIPES" if player1_group == "stripes" else "???")
        p2_type = "STRIPES" if player1_group == "solids" else ("SOLIDS" if player1_group == "stripes" else "???")

        # PANEL PLAYER 1
        p1_rect = pygame.Rect(20 * SCALE, 10 * SCALE, 400 * SCALE, header_height - (20 * SCALE))
        border_col_1 = ACTIVE_BORDER if current_player == 1 else GREY
        border_thick_1 = 3 if current_player == 1 else 1
        pygame.draw.rect(screen, UI_BG, p1_rect, border_radius=10)
        pygame.draw.rect(screen, border_col_1, p1_rect, border_thick_1, border_radius=10)
        
        col_1 = YELLOW if current_player == 1 else GREY
        import config as conf
        draw_text(screen, f"PLAYER 1 ({p1_type})", conf.font, col_1, p1_rect.x + 15, p1_rect.y + 10)
        
        ball_start_x = p1_rect.x + 15
        ball_start_y = p1_rect.y + 45 * SCALE
        for i, ball_img in enumerate(potted_balls_1):
            screen.blit(ball_img, (ball_start_x + (i * (35 * SCALE)), ball_start_y))

        # PANEL PLAYER 2
        p2_width = 400 * SCALE
        p2_rect = pygame.Rect(SCREEN_WIDTH - p2_width - (20 * SCALE), 10 * SCALE, p2_width, header_height - (20 * SCALE))
        border_col_2 = ACTIVE_BORDER if current_player == 2 else GREY
        border_thick_2 = 3 if current_player == 2 else 1
        pygame.draw.rect(screen, UI_BG, p2_rect, border_radius=10)
        pygame.draw.rect(screen, border_col_2, p2_rect, border_thick_2, border_radius=10)

        col_2 = BLUE if current_player == 2 else GREY
        p2_text = f"PLAYER 2 ({p2_type})"
        p2_text_surf = conf.font.render(p2_text, True, col_2)
        screen.blit(p2_text_surf, (p2_rect.right - p2_text_surf.get_width() - 15, p2_rect.y + 10))

        ball_start_x_2 = p2_rect.right - 15 - (36 * SCALE) 
        ball_y_2 = p2_rect.y + 45 * SCALE
        for i, ball_img in enumerate(potted_balls_2):
            screen.blit(ball_img, (ball_start_x_2 - (i * (35 * SCALE)), ball_y_2))

        # STATUS TENGAH
        center_text = f"TURN: PLAYER {current_player}"
        center_surf = conf.large_font.render(center_text, True, WHITE)
        center_rect = center_surf.get_rect(center=(SCREEN_WIDTH/2, header_height/2))
        screen.blit(center_surf, center_rect)