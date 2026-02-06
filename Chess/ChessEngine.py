import chess
import pygame as pg
from pygame_gui import UIManager
from pygame_gui.elements import UITextBox, UIScrollingContainer
import ChessVisuals as cv
# this will be for all of the game logic

class ChessEngine:
    def __init__(self):
        pass

    font = pg.font.SysFont("arial", 20, True)
    large_font = pg.font.SysFont("arial", 35, True)
    FPS = 24
    moves_history = []

    #Logic

    # ENUM type for game mode with defaults
    GAME_PLAYING = 0
    GAME_PROMOTION = 1
    game_state = GAME_PLAYING
    pending_move = None

    # Methods for creating the game
    # Make board
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = cv.SQUARE_COLORS[(row + col) % 2]
                pg.draw.rect(cv.screen, color, pg.Rect(col * (cv.WIDTH / 8), row * (cv.HEIGHT / 8), cv.WIDTH / 8, cv.HEIGHT / 8))

    # Update the pieces and the board
    def draw_pieces(self, main_screen, board_state):
        for square in chess.SQUARES:
            piece = board_state.piece_at(square)
            if piece:
                file_index = chess.square_file(square)
                rank_index = 7 - chess.square_rank(square)  # Pygame y-axis is top down
                main_screen.blit(cv.PIECE_IMAGES[piece.symbol()], (file_index * (cv.WIDTH / 8), rank_index * (cv.HEIGHT / 8)))

    def mouse_to_square(self, position):
        # Add mouse click logic
        x, y = position
        file = int(x // (cv.WIDTH / 8))
        rank = 7 - int(y // (cv.HEIGHT / 8))
        return chess.square(file, rank)

    # Highlight the square selected
    def draw_selected_square(self, square):
        if square is None:
            return
        file = chess.square_file(square)
        rank = 7 - chess.square_rank(square)

        highlight = pg.Surface((cv.WIDTH / 8, cv.HEIGHT / 8), pg.SRCALPHA)
        highlight.fill((255, 255, 0, 100))
        cv.screen.blit(highlight, (file * (cv.WIDTH / 8), rank * (cv.HEIGHT / 8)))

    #Show whos turn it is
    def draw_turn(self, turn):
        turn_surface = self.large_font.render("Turn: " + str(turn), True, cv.WHITE)
        textX = (950 - (turn_surface.get_width() / 2))
        textY = 10
        cv.screen.blit(turn_surface, (textX, textY))

    # Right side information box
    def draw_information(self):
        black_box = pg.Rect(700, 0, 500, 800)
        cv.screen.blit(cv.information_surface, black_box)

        # Draw quit button
        cv.screen.blit(cv.red_surface, cv.quit_rect)
        cv.screen.blit(self.large_font.render("QUIT", True, cv.WHITE),
        (cv.pos_x + (cv.size_x / 3), cv.pos_y + (cv.size_y / 6), cv.size_x, cv.size_y))

    # Ask to promote
    def draw_promotion(self):
        print("promo!")
        # Draw the options
        promo_text = self.font.render("Choose a promotion", True, cv.WHITE)
        cv.screen.blit(promo_text, (950 - (promo_text.get_width() / 2), 50))

        # img location and size
        x = 750
        y = 100
        size = 100

        # Draw options
        for key, img in cv.promotion_options.items():
            rect = pg.Rect(x, y, size, size)
            cv.promotion_rects[key] = rect
            cv.screen.blit(img, rect)
            x += size + 10

    def add_move_to_log(self, move):
        self.moves_history.append(str(move))

        html = "<br>".join(self.moves_history)
        cv.moves_text.set_text(html)