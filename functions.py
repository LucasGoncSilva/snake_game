from pygame import quit as pg_quit
from constants import WIN_SIZE

def collision(pos_a: tuple, pos_b: tuple) -> bool: return pos_a == pos_b


def off_limits(pos: tuple) -> bool:
    if 0 <= pos[0] <= WIN_SIZE[0] and 0 <= pos[1] <= WIN_SIZE[1]:
        return False
    else: return True


def exit_game() -> None:
    pg_quit()
    quit()