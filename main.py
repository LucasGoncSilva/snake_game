from datetime import datetime

import pygame as pg

from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_UP, \
    K_DOWN, K_LEFT, K_RIGHT, K_r, K_q

from pygame_menu import Theme, Menu, events, sound

from constants import *
from classes import Snake, Apple, LimitedArea, Score
from functions import *


pg.init()

win = pg.display.set_mode(WIN_SIZE)
pg.display.set_caption('Snake Game')


snake = Snake()
apple = Apple()
area = LimitedArea()
score = Score()


def restart():
    snake.regenerate()
    apple.regenerate()
    score.reset()
    run()


def run():
    while 1:
        # loop constants
        pg.time.Clock().tick(15)
        win.fill(MAIN_COLOR)
        font = pg.font.Font(r'.\fonts\PixeloidSans-nR3g1.ttf', 30)


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
                
                elif event.key == K_r and not snake.walking:
                    restart()


        # collisions detection
        if collision(snake.head(), apple.pos):
            score.add()
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

        pg.draw.rect(
            win,
            area.color,
            pg.Rect(
                area.left,
                area.top,
                area.width,
                area.height
            ),
            area.border
        )

        if snake.walking:
            score_text = font.render(
                f'Score: {score.value}',
                True,
                ACCENT_COLOR2
            )
            score_text_rect = score_text.get_rect()
            score_text_rect.left = area.left
            score_text_rect.top = area.left
            win.blit(score_text, score_text_rect)

        else:
            if datetime.now().second % 2 == 0:
                lose_text = font.render(
                    f'Score: {score.value} points! Press "r" to restart!',
                    True,
                    RED
                )
            else:
                lose_text = font.render(
                    f'Score: {score.value} points! Press "r" to restart!',
                    True,
                    ACCENT_COLOR2
                )

            lose_text_rect = lose_text.get_rect()
            lose_text_rect.center = (WIN_SIZE[0] / 2, (area.top) / 2)
            win.blit(lose_text, lose_text_rect)

        pg.display.update()


theme = Theme(
    # general
    selection_color = ACCENT_COLOR2,
    # title
    title = True,
    title_font = r'.\fonts\PixeloidSans-nR3g1.ttf',
    title_font_color = MAIN_COLOR,
    title_background_color = ACCENT_COLOR2,
    # background
    background_color = MAIN_COLOR,
    # widget
    widget_font = r'.\fonts\PixeloidSans-nR3g1.ttf',
    widget_font_color = ACCENT_COLOR1
)

engine = sound.Sound()
engine.set_sound(sound.SOUND_TYPE_KEY_ADDITION, '.\sounds\menu.wav')

menu = Menu('Snake Game', WIN_SIZE[0], WIN_SIZE[1], theme=theme)
menu.set_sound(engine)

menu.add.button('Play', run)
menu.add.button('Quit', events.EXIT)
menu.add.vertical_margin(20, 'm')
menu.add.label('Arrow Keys to move:\n◄▲▼►')

menu.mainloop(win)