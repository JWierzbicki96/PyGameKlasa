"""Author: [Jakub Wierzbicki]
Date: [14.01.2025]
Course: Python I, Lab 6/7
Assignent: [Ćwiczenia składni w programowaniu proceduralnym z wykorzystaniem elementów graficznych Pygame]
Description: [Gra opierjąca się na bibiotece Pygame. Gra która polega na przejściu planszy dzięki wyrzuceniu odpowiedniej
ilości oczek na kostce. Gra posiada pola, które cofają lub powodują restart gry]
Version: [Wersja 3.12]
Dificulty: [średnie]
The level of motivation to learn Python: [Bardzo wysoki]
Expected mark: [5]
Own ideas for modifying task, suggestions of your own: [-]
Other notes, own observations: [brak]
"""

import pygame
import random

class GameConfig:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (100, 149, 237)
    GREEN = (34, 139, 34)
    RED = (255, 69, 0)
    YELLOW = (255, 223, 0)
    FONT_SIZE = 36
    BOARD_SIZE_X = 12
    BOARD_SIZE_Y = 6
    CELL_SIZE = SCREEN_WIDTH // BOARD_SIZE_X

class Board:
    def __init__(self, config, font):
        self.config = config
        self.font = font
        self.special_tiles = {
            5: {"color": self.config.GREEN, "effect": -2},  # Przykład specjalnego pola
            10: {"color": self.config.RED, "effect": 3},
            15: {"color": self.config.YELLOW, "effect": -5}
        }
        self.bomb_position = 20  # Przykładowa pozycja bomby

    def draw(self, screen):
        for row in range(self.config.BOARD_SIZE_Y):
            for col in range(self.config.BOARD_SIZE_X):
                tile_number = row * self.config.BOARD_SIZE_X + col + 1
                x, y = col * self.config.CELL_SIZE, row * self.config.CELL_SIZE + 150
                color = self.config.WHITE

                if tile_number in self.special_tiles:
                    color = self.special_tiles[tile_number]["color"]
                if tile_number == self.bomb_position:
                    color = (255, 0, 255)

                pygame.draw.rect(screen, color, (x, y, self.config.CELL_SIZE, self.config.CELL_SIZE))
                pygame.draw.rect(screen, self.config.BLACK, (x, y, self.config.CELL_SIZE, self.config.CELL_SIZE), 2)

                text = self.font.render(str(tile_number), True, self.config.BLACK)
                text_rect = text.get_rect(center=(x + self.config.CELL_SIZE // 2, y + self.config.CELL_SIZE // 2))
                screen.blit(text, text_rect)


class Player:
    def __init__(self, config, font):
        self.config = config
        self.font = font
        self.position = 1

    def move(self, steps, board):
        self.position += steps

        if self.position in board.special_tiles:
            effect = board.special_tiles[self.position]["effect"]
            self.position = max(1, self.position + effect)

        if self.position == board.bomb_position:
            self.position = 1

    def draw(self, screen):
        row = (self.position - 1) // self.config.BOARD_SIZE_X
        col = (self.position - 1) % self.config.BOARD_SIZE_X

        x, y = col * self.config.CELL_SIZE, row * self.config.CELL_SIZE + 150
        pygame.draw.circle(screen, self.config.BLUE, (x + self.config.CELL_SIZE // 2, y + self.config.CELL_SIZE // 2), self.config.CELL_SIZE // 4)


class Game:
    def __init__(self):
        pygame.init()
        self.config = GameConfig()
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        pygame.display.set_caption("Gra Planszowa")

        self.font = pygame.font.Font(None, self.config.FONT_SIZE)


        self.board = Board(self.config, self.font)
        self.player = Player(self.config, self.font)
        self.dice_roll = None
        self.roll_count = 0
        self.game_over = False


    def roll_dice(self):
        self.dice_roll = random.randint(1, 6)
        self.player.move(self.dice_roll, self.board)
        self.roll_count += 1

        if self.player.position >= self.config.BOARD_SIZE_X * self.config.BOARD_SIZE_Y:
            self.player.position = self.config.BOARD_SIZE_X * self.config.BOARD_SIZE_Y
            self.game_over = True

    def run(self):
        running = True
        while running:
            self.screen.fill(self.config.WHITE)
            self.board.draw(self.screen)
            self.player.draw(self.screen)

            if self.dice_roll is not None:
                self.draw_dice()

            self.draw_text(f"Rzuty kostką: {self.roll_count}", 10, 130)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.roll_dice()

            pygame.display.flip()

        pygame.quit()

    def draw_dice(self):
        pygame.draw.rect(self.screen, self.config.WHITE, (650, 50, 80, 80), border_radius=10)
        pygame.draw.rect(self.screen, self.config.BLACK, (650, 50, 80, 80), 3, border_radius=10)
        text = self.font.render(str(self.dice_roll), True, self.config.BLACK)  # Używamy self.font
        text_rect = text.get_rect(center=(690, 90))
        self.screen.blit(text, text_rect)

    def draw_text(self, text, x, y, color=None):
        if color is None:
            color = self.config.BLACK
        render = self.font.render(text, True, color)  # Używamy self.font
        self.screen.blit(render, (x, y))

if __name__ == "__main__":
    game = Game()
    game.run()

