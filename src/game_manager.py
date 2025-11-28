import math

class GameManager:
    def __init__(self):
        self.force = 0
        self.max_force = 10000
        self.powering_up = False
        self.pull_start_pos = (0, 0)

        self.aim_locked = False
        self.locked_angle = 0

    def mouse_down(self, cue_ball_pos, mouse_pos):
        self.powering_up = True
        self.pull_start_pos = mouse_pos
        self.force = 0

        dx = cue_ball_pos[0] - mouse_pos[0]
        dy = -(cue_ball_pos[1] - mouse_pos[1])
        self.locked_angle = math.degrees(math.atan2(dy, dx))
        self.aim_locked = True

    def mouse_up_start_animation(self):
        """
        Dipanggil saat mouse dilepas — ini hanya menandakan mulai animasi di main.
        main akan memeriksa self.force untuk final_force.
        """
        self.powering_up = False
        # jangan reset force di sini (force akan dipakai saat impact dan di-reset setelah impact)

    def update_power(self, mouse_pos):
        if not self.powering_up:
            return 0, 0
        dx = mouse_pos[0] - self.pull_start_pos[0]
        dy = mouse_pos[1] - self.pull_start_pos[1]
        dist = (dx*dx + dy*dy)**0.5
        sensitivity = 35
        self.force = min(dist * sensitivity, self.max_force)
        visual_offset = min(dist, 300)
        return dist, visual_offset
