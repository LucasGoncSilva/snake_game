import pygame as pg
from pygame.locals import *

from constants import *
from classes import Snake, Apple, LimitedArea
from functions import *


pg.init()


win = pg.display.set_mode(WIN_SIZE)
pg.display.set_caption('Snake Game')


snake = Snake()
apple = Apple()
area = LimitedArea()


while 1:
    # loop constants
    pg.time.Clock().tick(15)
    win.fill(MAIN_COLOR)


    # event detection
    for event in pg.event.get():
        if event.type == QUIT: exit_game()

        if event.type == KEYDOWN:
            if event.key == K_q or event.key == K_ESCAPE: exit_game()

            elif event.key == K_UP and snake.direction != K_DOWN:
                snake.go_to(K_UP)

            elif event.key == K_DOWN and snake.direction != K_UP:
                snake.go_to(K_DOWN)

            elif event.key == K_RIGHT and snake.direction != K_LEFT:
                snake.go_to(K_RIGHT)

            elif event.key == K_LEFT and snake.direction != K_RIGHT:
                snake.go_to(K_LEFT)


    # collisions detection
    if collision(snake.head(), apple.pos):
        snake.grow()
        apple.regenerate()

        for pos in snake.body():
            if collision(pos, apple.pos):
                apple.regenerate()
    
    if area.off_limits(snake.head()):
        snake.stop()


    # draw
    snake.walk()

    for i, pos in enumerate(snake.full_body()):
        if i % 2 != 1:
            win.blit(snake.skin1, pos)
        else:
            win.blit(snake.skin2, pos)
    
    win.blit(apple.surface, apple.pos)

    pg.draw.rect(win, area.color, pg.Rect(area.left, area.top, area.width, area.height), area.border)
    # pg.draw.rect(win, area.color, pg.Rect(45, 40, 600, 585), area.border)
    
    pg.display.update()