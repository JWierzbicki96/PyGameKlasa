# Gra Planszowa w Python (Pygame)

## Opis projektu
Jest to prosta gra planszowa napisana w Pythonie z użyciem biblioteki Pygame. Gracz porusza się po planszy, rzucając kostką i przesuwając pionek o odpowiednią liczbę oczek.
Na planszy znajdują się specjalne pola, które mogą przyspieszyć ruch (zielone pola) lub cofnąć gracza (czerwone pola). Dodatkowo na środku planszy znajduje się "bomba", 
która resetuje grę, jeśli na nią trafisz.

## Funkcjonalności
- Rzut kostką (1-6 oczek) przy użyciu klawisza SPACJA
- Plansza o wymiarach 12x6 pól
- Specjalne pola dające bonusy lub kary ruchu
- Reset pozycji gracza po trafieniu na bombę
- Informacje o pozycji gracza, wyniku rzutu i liczbie rzutów
- Komunikat o wygranej po dojściu do końca planszy

## Wymagania
- Python 3.12
- Biblioteka Pygame (można zainstalować przez `pip install pygame`)

## Jak uruchomić grę
1. Sklonuj repozytorium lub pobierz pliki.
2. Upewnij się, że masz zainstalowany Python i Pygame.
3. Uruchom plik `main.py`:
