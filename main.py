"""Author: [Jakub Wierzbicki]
Date: [14.01.2025]
Assignent: [Programowanie proceduralnw z wykorzystaniem elementów graficznych Pygame]
Description: [Gra opierjąca się na bibiotece Pygame. Gra która polega na przejściu planszy dzięki wyrzuceniu odpowiedniej
ilości oczek na kostce. Gra posiada pola, które cofają lub powodują restart gry]
Version: [Wersja 3.12]
"""

import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gra Planszowa")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GREEN = (34, 139, 34)
RED = (255, 69, 0)
YELLOW = (255, 223, 0)

# Czcionka
font = pygame.font.Font(None, 36)

# Zmienne gry
board_size_x = 12  # 12 kolumn
board_size_y = 6  # 6 wierszy
cell_size = SCREEN_WIDTH // board_size_x
player_position = 1
game_over = False
dice_roll = None
roll_count = 0  # Licznik rzutów kostką

# Pola specjalne :Zielone pole: +3, Czerwone pole: -2

special_tiles = {
    5: {"color": GREEN, "effect": 3},
    10: {"color": RED, "effect": -2},
    18: {"color": GREEN, "effect": 3},
    24: {"color": RED, "effect": -2},
    30: {"color": GREEN, "effect": 3},
    40: {"color": RED, "effect": -2},
    50: {"color": RED, "effect": -2},
    60: {"color": RED, "effect": -2},
}

# Bomba na środku planszy
bomb_position = (board_size_x * board_size_y) // 2  # Środkowe pole planszy


# Funkcja rysująca planszę
def draw_board():
    for row in range(board_size_y):
        for col in range(board_size_x):
            tile_number = row * board_size_x + col + 1
            x, y = col * cell_size, row * cell_size + 150  # Przesunięcie wierszy o 150, żeby napisy nie nachodziły na planszę

            # Kolor specjalnych pól
            color = WHITE
            if tile_number in special_tiles:
                color = special_tiles[tile_number]["color"]
            if tile_number == bomb_position:
                color = (255, 0, 255)  # Fioletowe pole dla bomby

            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
            pygame.draw.rect(screen, BLACK, (x, y, cell_size, cell_size), 2)

            # Numer pola
            text = font.render(str(tile_number), True, BLACK)
            text_rect = text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
            screen.blit(text, text_rect)


# Funkcja rysująca pionek gracza
def draw_player(position):
    row = (position - 1) // board_size_x
    col = (position - 1) % board_size_x

    x, y = col * cell_size, row * cell_size + 150  # Przesunięcie pionka, aby był w odpowiednim miejscu na planszy
    pygame.draw.circle(screen, BLUE, (x + cell_size // 2, y + cell_size // 2), cell_size // 4)


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
