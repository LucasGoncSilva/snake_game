from random import randint


from pygame import Surface
from pygame.mixer import music
from pygame.locals import *

from constants import *


class Snake:
    def __init__(self) -> None:
        x = WIN_SIZE[0] // 2 // PX_SIZE * PX_SIZE
        y = WIN_SIZE[1] // 2 // PX_SIZE * PX_SIZE
        self.pos = [
            (x, y),
            (x + PX_SIZE, y),
            (x + PX_SIZE * 2, y)
        ]

        self.skin1 = Surface((PX_SIZE, PX_SIZE))
        self.skin1.fill(SECONDARY_COLOR)

        self.skin2 = Surface((PX_SIZE, PX_SIZE))
        self.skin2.fill(ACCENT_COLOR1)

        self.direction = K_LEFT

        self.walking = 1
        self.collided = 0

    def head(self) -> tuple:
        return self.pos[0]
    
    def body(self) -> list:
        return self.pos[1:]

    def full_body(self) -> list:
        return self.pos

    def go_to(self, direction: object) -> None:
        if self.walking and self.direction != direction:
            self.direction = direction
            music.load('sounds/walk.wav')
            music.play(0)
    
    def walk(self) -> None:
        if self.walking:
            for i in range(len(self.pos) - 1, 0, -1):
                if self.collision(self.pos[0], self.pos[i]):
                    self.stop()
                    return
                self.pos[i] = self.pos[i - 1]

            if self.direction == K_UP:
                self.pos[0] = (self.pos[0][0], self.pos[0][1] - PX_SIZE)
            elif self.direction == K_DOWN:
                self.pos[0] = (self.pos[0][0], self.pos[0][1] + PX_SIZE)
            elif self.direction == K_RIGHT:
                self.pos[0] = (self.pos[0][0] + PX_SIZE, self.pos[0][1])
            elif self.direction == K_LEFT:
                self.pos[0] = (self.pos[0][0] - PX_SIZE, self.pos[0][1])

    def grow(self) -> None:
        self.pos.append((-1 - PX_SIZE, -1 - PX_SIZE))
        music.load('sounds/eat.wav')
        music.play(0)
    
    def collision(self, pos_a: tuple, pos_b: tuple) -> bool: return pos_a == pos_b

    def stop(self) -> None:
        if self.walking == 1:
            self.walking = 0
            music.load('sounds/lose.wav')
            music.play(0)


class Apple:
    def __init__(self) -> None:
        x = randint(0, WIN_SIZE[0])
        y = randint(0, WIN_SIZE[1])
        self.pos = (x // PX_SIZE * PX_SIZE, y // PX_SIZE * PX_SIZE)

        self.surface = Surface((PX_SIZE, PX_SIZE))
        self.surface.fill(RED)

    def regenerate(self) -> None:
        x = randint(0, WIN_SIZE[0])
        y = randint(0, WIN_SIZE[1])
        self.pos = (x // PX_SIZE * PX_SIZE, y // PX_SIZE * PX_SIZE)