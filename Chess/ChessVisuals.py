import pygame as pg
from pygame_gui import UIManager
from pygame_gui.elements import UITextBox, UIScrollingContainer
#Surfaces also go in here
#Colors for players and board
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SQUARE_COLORS = ((255, 255, 255), (50, 50, 50)) #For the board squares

WIDTH, HEIGHT = 700, 700
screen = pg.display.set_mode((1200, HEIGHT))

information_surface = pg.Surface((500, 800))
information_surface.fill((0, 0, 0)) # information background color. If not set, it's default is black
red_surface = pg.Surface((200, 50))
red_surface.fill((255, 0, 0))

#Quit button/rect
size_x = 200
size_y = 50
pos_x = 850
pos_y = 630
quit_rect = pg.Rect(pos_x, pos_y, size_x, size_y)

promotion_rects = {}

#Load images for promo and piece
promotion_options =    {'r': pg.image.load("white-rook.png"),
                        'n': pg.image.load("white-knight.png"),
                        'b': pg.image.load("white-bishop.png"),
                        'q': pg.image.load("white-queen.png")
                        }
#load pieces
PIECE_IMAGES =       {'P': pg.image.load("white-pawn.png"),
                      'R': pg.image.load("white-rook.png"),
                      'N': pg.image.load("white-knight.png"),
                      'B': pg.image.load("white-bishop.png"),
                      'Q': pg.image.load("white-queen.png"),
                      'K': pg.image.load("white-king.png"),
                      'p': pg.image.load("black-pawn.png"),
                      'r': pg.image.load("black-rook.png"),
                      'n': pg.image.load("black-knight.png"),
                      'b': pg.image.load("black-bishop.png"),
                      'q': pg.image.load("black-queen.png"),
                      'k': pg.image.load("black-king.png"), }

#Resizing normal pieces
new_size = (90, 90)
for each in PIECE_IMAGES:
    PIECE_IMAGES[each] = pg.transform.scale(PIECE_IMAGES[each], new_size)

#Resizing promo pieces
for each in promotion_options:
    promotion_options[each] = pg.transform.scale(promotion_options[each], (80, 80))


ui_manager = UIManager((1200, HEIGHT), None)

# Text box for move updates
moves_rect = pg.Rect(850, 400, 200, 200)

moves_container = UIScrollingContainer(
    relative_rect=moves_rect,
    manager=ui_manager,
    should_grow_automatically=True
)
moves_text = UITextBox(
    html_text="",
    relative_rect=pg.Rect(0, 0, 430, 200),
    manager=ui_manager,
    container=moves_container,
    placeholder_text="Moves List"
)