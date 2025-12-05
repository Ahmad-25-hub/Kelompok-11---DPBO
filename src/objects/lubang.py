from config import *

pocket_dia = int(66 * SCALE)

raw_pockets_orig = [
    (55, 63), (592, 48), (1134, 64),
    (55, 616), (592, 629), (1134, 616)
]

pockets = []
for p in raw_pockets_orig:
    px = (p[0] * SCALE) + MARGIN_X
    py = (p[1] * SCALE) + MARGIN_Y
    pockets.append((px, py))