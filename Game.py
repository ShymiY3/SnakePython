import pygame as pg
from Game_objects import *
import sys

GAME_OVER = pg.USEREVENT + 1
pg.display.set_caption("SnakePython")

class Game:
    def __init__(self) -> None:
        pg.init()
        self.WINDOW_WIDTH = 10*32
        self.WINDOW_HEIGHT = 8*32
        self.TILE_SIZE = 32
        self.screen = pg.display.set_mode(
            [self.WINDOW_WIDTH, self.WINDOW_HEIGHT])
        self.screen_rect = pg.rect.Rect(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.clock = pg.time.Clock()
        self.new_game()

    def new_game(self):
        self.snake = Snake(self)
        self.food = Food(self, self.snake)

    def update(self):
        self.snake.update()
        pg.display.flip()

    def draw(self):
        self.screen.fill('#c9a35d')
        if((self.snake.length >= (self.WINDOW_HEIGHT//self.TILE_SIZE) * (self.WINDOW_WIDTH//self.TILE_SIZE))-1):
            self.food.draw()
        self.snake.draw()


    def snake_eats(self):
        if self.snake.rect.colliderect(self.food.rect):
            self.snake.length += 1
            self.food.update()

    def collision(self):
        if self.snake.length > 2:
            if self.snake.rect.collidelist(self.snake.segments[:-1]) != -1:
                pg.event.post(pg.event.Event(GAME_OVER))
                self.snake.segments.pop()
                self.snake.segments.insert(0,self.snake.last_segm)
        if self.snake.rect.x >= self.WINDOW_WIDTH or self.snake.rect.x < 0 or self.snake.rect.y >= self.WINDOW_HEIGHT or self.snake.rect.y < 0:
            pg.event.post(pg.event.Event(GAME_OVER))
            self.snake.segments.pop()
            self.snake.segments.insert(0,self.snake.last_segm)
        

    def pauseMassage(self, text, fade_time):
        paused = True
        font = pg.font.Font(None, self.WINDOW_WIDTH//5)
        blue = pg.Color('#525252')
        orig_surf = font.render(text, True, blue)
        txt_surf = orig_surf.copy()
        alpha_surf = pg.Surface(txt_surf.get_size(), pg.SRCALPHA)
        alpha = 0
        pg.time.set_timer(pg.USEREVENT, fade_time//64)
        

        while paused:
            for event in pg.event.get():
                if event.type == pg.USEREVENT:
                    if alpha < 255:
                        alpha = min(alpha+4, 255)
                        txt_surf = orig_surf.copy()
                        alpha_surf.fill((255,255,255, alpha))
                        txt_surf.blit(alpha_surf, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
                    self.draw()
                    rect = txt_surf.get_rect(center=self.screen_rect.center)
                    self.screen.blit(txt_surf, rect)
                    pg.display.flip()

                if event.type == pg.KEYDOWN:
                    paused = False

                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

    def check_event(self):
        self.snake_eats()
        self.collision()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == GAME_OVER:
                if (self.snake.length >= (self.WINDOW_HEIGHT//self.TILE_SIZE) * (self.WINDOW_WIDTH//self.TILE_SIZE)):
                    self.pauseMassage("You Won", 3000)
                
                else:
                    self.pauseMassage("Game Over", 3000)

                self.new_game()

            self.snake.control(event)

    def run(self):
        while True:
            self.clock.tick(120)
            self.check_event()
            self.update()
            self.draw()
