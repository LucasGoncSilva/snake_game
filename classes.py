from random import randint
import sqlite3

from pygame import Surface
from pygame.mixer import music
from pygame.locals import *

from constants import *


class Area:
    def __init__(self) -> None:
        self.width, self.height = LIMIT_AREA

        self.left = (WIN_SIZE[0] - self.width + PX_SIZE) / 2 // PX_SIZE * PX_SIZE
        self.top = (WIN_SIZE[1] - self.height - self.left) // PX_SIZE * PX_SIZE
        self.right = self.left + self.width
        self.bottom = self.top + self.height


class LimitedArea(Area):
    def __init__(self) -> None:
        Area.__init__(self)

        self.border = PX_SIZE
        self.color = ACCENT_COLOR2

    def off_limits(self, pos: tuple) -> bool:
        if self.left < pos[0] < self.right - PX_SIZE and \
            self.top < pos[1] < self.bottom - PX_SIZE:
            return False
        else: return True


class Snake(Area):
    def __init__(self) -> None:
        Area.__init__(self)

        x = (self.right + self.left) // 2 // PX_SIZE * PX_SIZE
        y = (self.bottom + self.top) // 2 // PX_SIZE * PX_SIZE

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
    
    def collision(self, pos_a: tuple, pos_b: tuple) -> bool:
        return pos_a == pos_b

    def stop(self) -> None:
        if self.walking == 1:
            self.walking = 0
            music.load('sounds/lose.wav')
            music.play(0)
    
    def regenerate(self) -> None:
        x = (self.right + self.left) // 2 // PX_SIZE * PX_SIZE
        y = (self.bottom + self.top) // 2 // PX_SIZE * PX_SIZE

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


class Apple(Area):
    def __init__(self) -> None:
        Area.__init__(self)

        x = randint(self.left + PX_SIZE, self.right - 2 * PX_SIZE)
        y = randint(self.top + PX_SIZE, self.bottom - 2 * PX_SIZE)
        self.pos = (x // PX_SIZE * PX_SIZE, y // PX_SIZE * PX_SIZE)

        self.surface = Surface((PX_SIZE, PX_SIZE))
        self.surface.fill(RED)

    def regenerate(self) -> None:
        x = randint(self.left + PX_SIZE, self.right - 2 * PX_SIZE)
        y = randint(self.top + PX_SIZE, self.bottom - 2 * PX_SIZE)
        self.pos = (x // PX_SIZE * PX_SIZE, y // PX_SIZE * PX_SIZE)


class Score:
    def __init__(self) -> None:
        self.value = 0
    
    def add(self) -> None: self.value += 1

    def reset(self) -> None: self.value = 0


class DataBase:
    def __init__(self) -> None:
        # self.db = sqlite3.connect('scores.db')
        self.db = sqlite3.connect(':memory:')
        self.query = self.db.cursor()

        self.query.execute(
            """CREATE TABLE IF NOT EXISTS
            scores (score INTEGER NOT NULL)
            """
        )

    def new(self, score: int) -> None:
        self.query.execute('INSERT INTO scores (score) VALUES (?)', (score,))
        self.save()

    def high(self) -> int:
        query, = self.query.execute('SELECT * FROM scores ORDER BY score DESC LIMIT 1')
        num, = query
        return num

    def compare(self) -> None:
        pass

    def save(self) -> None:
        self.db.commit()

    def save2go(self) -> None:
        self.db.commit()
        self.db.close()