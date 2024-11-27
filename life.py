import pygame
import random
import numpy as np 
from enum import Enum

pygame.init()
font = pygame.font.Font('game_of_life\Arialn.ttf', 25)
font_color = pygame.Color('white')

class GameLife:
    def __init__(self, width = 920, height = 640, resolution = 10, fps = 40):
        self.width = width
        self.height = height
        self.resolution = resolution
        self.fps = fps
        self.grid = np.array([[random.choice([0, 1]) for i in range(self.width//self.resolution)] for j in range(self.height//self.resolution)])
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.exit_button = Button(10, 10, 100, 50, 'Exit', (0, 255, 0))
        self.speed_up_button = Button(120, 10, 100, 50, '+', (0, 255, 0))
        self.speed_down_button = Button(230, 10, 100, 50, '-', (0, 255, 0))

    def update_life(self):
        new_grid = self.grid.copy()
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                neighbours = self.count_neighbours(i, j)
                if self.grid[i][j] == 1:
                    if neighbours < 2 or neighbours > 3:
                        new_grid[i][j] = 0
                else:
                    if neighbours == 3:
                        new_grid[i][j] = 1
        self.grid = new_grid
        self.draw()

    def count_neighbours(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if x+i >= 0 and x+i < self.grid.shape[0] and y+j >= 0 and y+j < self.grid.shape[1]:
                    if self.grid[x+i][y+j] == 1:
                        count += 1
        return count

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, (255, 255, 255), (j*self.resolution, i*self.resolution, self.resolution-1, self.resolution-1))
        self.exit_button.draw(self.screen)
        self.speed_up_button.draw(self.screen)
        self.speed_down_button.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(self.fps)

    def update_UI(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.exit_button.click(pos):
                    pygame.quit()
                    quit()
                if self.speed_up_button.click(pos):
                    if self.fps < 40:
                        self.fps = 40
                    elif self.fps < 60:
                        self.fps = 60
                    elif self.fps < 100:
                        self.fps = 100

                if self.speed_down_button.click(pos):
                    if self.fps > 60:
                        self.fps = 60
                    elif self.fps > 40:
                        self.fps = 40
                    elif self.fps > 10:
                        self.fps = 10

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.exit_button.hover(pos)
                self.speed_up_button.hover(pos)
                self.speed_down_button.hover(pos)

        self.clock.tick(self.fps)

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text = font.render(self.text, 1, font_color)
        screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def hover(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.color = (255, 0, 0)
                return True
        self.color = (0, 0, 0)
        return False

    def click(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


if __name__ == '__main__':
    game = GameLife(width=1080, height=720, resolution=15, fps=40)

    while True:
        game.update_UI()
        game.update_life()

    pygame.quit()