import pygame as pg
from random import randrange, choice
import os
from itertools import product

vec = pg.math.Vector2


class Textures:
    def __init__(self, game) -> None:
        self.TEXTURE = {
            # U - UP
            "HEAD_U": (3*game.TILE_SIZE, 0, game.TILE_SIZE, game.TILE_SIZE),
            # D - DOWN
            "HEAD_D": (4*game.TILE_SIZE, game.TILE_SIZE, game.TILE_SIZE, game.TILE_SIZE),
            # R - LEFT
            "HEAD_R": (4*game.TILE_SIZE, 0, game.TILE_SIZE, game.TILE_SIZE),
            # L - RIGHT
            "HEAD_L": (3*game.TILE_SIZE, game.TILE_SIZE, game.TILE_SIZE, game.TILE_SIZE),
            "TAIL_U": (3*game.TILE_SIZE, 2*game.TILE_SIZE, game.TILE_SIZE, game.TILE_SIZE),
            "TAIL_D": (4*game.TILE_SIZE, 3*game.TILE_SIZE, game.TILE_SIZE, game.TILE_SIZE),
            "TAIL_R": (4*game.TILE_SIZE, 2*game.TILE_SIZE, game.TILE_SIZE, game.TILE_SIZE),
            "TAIL_L": (3*game.TILE_SIZE, 3*game.TILE_SIZE, game.TILE_SIZE, game.TILE_SIZE),
            "CURVED_UL": (0, 0, game.TILE_SIZE, game.TILE_SIZE),
            "CURVED_DL": (0, game.TILE_SIZE, game.TILE_SIZE, game.TILE_SIZE),
            "CURVED_UR": (2*game.TILE_SIZE, 0, game.TILE_SIZE, game.TILE_SIZE),
            "CURVED_DR": (2*game.TILE_SIZE, 2*game.TILE_SIZE, game.TILE_SIZE, game.TILE_SIZE),
            "BODY_V": (2*game.TILE_SIZE, game.TILE_SIZE, game.TILE_SIZE, game.TILE_SIZE),
            "BODY_H": (game.TILE_SIZE, 0, game.TILE_SIZE, game.TILE_SIZE),
            "APPLE": (0, 3*game.TILE_SIZE, game.TILE_SIZE, game.TILE_SIZE)
        }
        self.skin = pg.image.load(os.path.join('assets', 'snake-graphics.png'))


class Food:
    def __init__(self, game, snake) -> None:
        self.game = game
        self.snake = snake
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect(0, 0, self.size, self.size)
        self.text = Textures(game)
        self.rect.topleft = self.rand_pos()

    def rand_pos(self):
        try:
            return choice(tuple(filter(lambda x: self.snake.free_spaces[x], self.snake.free_spaces.keys())))
        except IndexError: return (-100,-100)
    def update(self):
        self.rect.topleft = self.rand_pos()

    def draw(self):
        self.game.screen.blit(
            self.text.skin, self.rect.topleft, self.text.TEXTURE.get('APPLE'))


class Snake:
    def __init__(self, game) -> None:
        self.game = game
        self.size = game.TILE_SIZE
        self.text = Textures(game)
        self.rect = pg.rect.Rect(0, 0, self.size, self.size)
        self.direction = vec(0, 0)
        self.rect.topleft = self.rand_pos()
        self.segments = [self.rect.copy()]
        self.length = 2
        self.time_now, self.time, self.time_step = 0, 0, 400
        self.free_spaces = {i: 1 for i in product(range(0, self.game.WINDOW_WIDTH, self.size), range(
            0, self.game.WINDOW_HEIGHT, self.size), repeat=1)}
        self.ind_ch = []
        self.last_segm = self.rect.copy()

    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and self.direction != vec(0, self.size):
                self.direction = vec(0, -self.size)
            if event.key == pg.K_s and self.direction != vec(0, -self.size):
                self.direction = vec(0, self.size)
            if event.key == pg.K_a and self.direction != vec(self.size, 0):
                self.direction = vec(-self.size, 0)
            if event.key == pg.K_d and self.direction != vec(-self.size, 0):
                self.direction = vec(self.size, 0)


    def rand_pos(self):
        return [randrange(self.size, self.game.WINDOW_WIDTH - self.size, self.size), randrange(self.size, self.game.WINDOW_HEIGHT - self.size, self.size)]

    def move(self):
        self.rect.move_ip(self.direction)

    def update(self):
        self.time_now = pg.time.get_ticks()
        if self.time_now - self.time > self.time_step:
            self.move()
            self.segments.append(self.rect.copy())
            self.ind_ch.clear()
            self.ind_ch.append(self.segments[0].topleft)
            self.ind_ch.append(self.segments[-1].topleft)
            if (self.ind_ch):
                self.free_spaces[self.ind_ch[0]] = 1
                self.free_spaces[self.ind_ch[1]] = 0
            self.last_segm = self.segments[0]
            self.segments = self.segments[-self.length:]
            self.time = self.time_now

    def draw(self):
        if self.direction == vec(0, 0):
            self.game.screen.blit(
                self.text.skin, self.rect.topleft, self.text.TEXTURE.get('HEAD_D'))
            self.game.screen.blit(self.text.skin, (self.rect.x, self.rect.y -
                                                   self.size), self.text.TEXTURE.get('TAIL_D'))
        for ind, seg in enumerate(self.segments):
            if seg == self.segments[-1]:
                if self.segments[ind-1].y > seg.y:
                    self.game.screen.blit(
                        self.text.skin, seg.topleft, self.text.TEXTURE.get('HEAD_U'))

                elif self.segments[ind-1].y < seg.y:
                    self.game.screen.blit(
                        self.text.skin, seg.topleft, self.text.TEXTURE.get('HEAD_D'))

                elif self.segments[ind-1].x < seg.x:
                    self.game.screen.blit(
                        self.text.skin, seg.topleft, self.text.TEXTURE.get('HEAD_R'))

                elif self.segments[ind-1].x > seg.x:
                    self.game.screen.blit(
                        self.text.skin, seg.topleft, self.text.TEXTURE.get('HEAD_L'))

            elif seg == self.segments[0]:
                if self.segments[ind+1].y < seg.y:
                    self.game.screen.blit(
                        self.text.skin, self.segments[0].topleft, self.text.TEXTURE.get('TAIL_U'))

                elif self.segments[ind+1].y > seg.y:
                    self.game.screen.blit(
                        self.text.skin, self.segments[0].topleft, self.text.TEXTURE.get('TAIL_D'))

                elif self.segments[ind+1].x > seg.x:
                    self.game.screen.blit(
                        self.text.skin, self.segments[0].topleft, self.text.TEXTURE.get('TAIL_R'))

                elif self.segments[ind+1].x < seg.x:
                    self.game.screen.blit(
                        self.text.skin, self.segments[0].topleft, self.text.TEXTURE.get('TAIL_L'))
            else:
                if self.segments[ind-1].y == self.segments[ind+1].y:
                    self.game.screen.blit(
                        self.text.skin, seg.topleft, self.text.TEXTURE.get('BODY_H'))
                elif self.segments[ind-1].x == self.segments[ind+1].x:
                    self.game.screen.blit(
                        self.text.skin, seg.topleft, self.text.TEXTURE.get('BODY_V'))
                elif seg.x > self.segments[ind-1].x and seg.y > self.segments[ind+1].y or seg.x > self.segments[ind+1].x and seg.y > self.segments[ind-1].y:
                    self.game.screen.blit(
                        self.text.skin, seg.topleft, self.text.TEXTURE.get('CURVED_DR'))
                elif seg.x < self.segments[ind-1].x and seg.y > self.segments[ind+1].y or seg.x < self.segments[ind+1].x and seg.y > self.segments[ind-1].y:
                    self.game.screen.blit(
                        self.text.skin, seg.topleft, self.text.TEXTURE.get('CURVED_DL'))
                elif seg.x > self.segments[ind-1].x and seg.y < self.segments[ind+1].y or seg.x > self.segments[ind+1].x and seg.y < self.segments[ind-1].y:
                    self.game.screen.blit(
                        self.text.skin, seg.topleft, self.text.TEXTURE.get('CURVED_UR'))
                elif seg.x < self.segments[ind-1].x and seg.y < self.segments[ind+1].y or seg.x < self.segments[ind+1].x and seg.y < self.segments[ind-1].y:
                    self.game.screen.blit(
                        self.text.skin, seg.topleft, self.text.TEXTURE.get('CURVED_UL'))
                else:
                    pg.draw.rect(self.game.screen, 'green', seg)
