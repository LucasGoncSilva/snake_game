from pygame import quit as pg_quit


def collision(pos_a: tuple, pos_b: tuple) -> bool: return pos_a == pos_b

def exit_game() -> None:
    pg_quit()
    quit()