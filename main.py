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
    FONT = pygame.font.Font(None, FONT_SIZE)

class Board:
    def __init__(self, config):
        self.config = config
        self.special_tiles = {
            5: {"color": config.GREEN, "effect": 3},
            10: {"color": config.RED, "effect": -2},
            18: {"color": config.GREEN, "effect": 3},
            24: {"color": config.RED, "effect": -2},
            30: {"color": config.GREEN, "effect": 3},
            40: {"color": config.RED, "effect": -2},
            50: {"color": config.RED, "effect": -2},
            60: {"color": config.RED, "effect": -2},
        }
        self.bomb_position = (config.BOARD_SIZE_X * config.BOARD_SIZE_Y) // 2

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

                text = self.config.FONT.render(str(tile_number), True, self.config.BLACK)
                text_rect = text.get_rect(center=(x + self.config.CELL_SIZE // 2, y + self.config.CELL_SIZE // 2))
                screen.blit(text, text_rect)


class Player:
    def __init__(self, config):
        self.config = config
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



# Funkcja rysująca kostkę
def draw_dice(roll):
    if roll is not None:
        pygame.draw.rect(screen, WHITE, (650, 50, 80, 80), border_radius=10)  # Przesunięcie kostki wyżej
        pygame.draw.rect(screen, BLACK, (650, 50, 80, 80), 3, border_radius=10)
        text = font.render(str(roll), True, BLACK)
        text_rect = text.get_rect(center=(690, 90))  # Zmiana pozycji tekstu w kostce
        screen.blit(text, text_rect)


# Funkcja wyświetlająca tekst na ekranie
def draw_text(text, x, y, color=BLACK):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))


# Główna pętla gry
running = True
while running:
    screen.fill(WHITE)

    # Rysowanie planszy
    draw_board()

    # Rysowanie pionka
    draw_player(player_position)

    # Rysowanie kostki
    draw_dice(dice_roll)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                # Rzut kostką
                dice_roll = random.randint(1, 6)
                player_position += dice_roll
                roll_count += 1  # Zwiększamy licznik rzutów

                # Sprawdzenie specjalnych pól
                if player_position in special_tiles:
                    effect = special_tiles[player_position]["effect"]
                    player_position = max(1, player_position + effect)

                # Sprawdzenie "bomby"
                if player_position == bomb_position:
                    player_position = 1  # Resetowanie gry, powrót na początek

                # Sprawdzenie końca gry
                if player_position >= board_size_x * board_size_y:
                    player_position = board_size_x * board_size_y
                    game_over = True

    # Rysowanie komunikatów
    draw_text("Gra Planszowa", 10, 10, YELLOW)
    draw_text(f"Pozycja gracza: {player_position}", 10, 50)

    if dice_roll is not None:
        draw_text(f"Rzut kostką: {dice_roll}", 10, 90)  # Przesunięcie napisu o rzucie kostką

    # Pozycja napisu o liczbie rzutów
    draw_text(f"Rzuty kostką: {roll_count}", 10, 130)  # Przesunięcie napisu w lewo

    # Napis gratulacyjny
    if game_over:
        draw_text("Gratulacje! Wygrałeś!", 250, 50, GREEN)

    pygame.display.flip()

# Zakończenie gry
pygame.quit()
