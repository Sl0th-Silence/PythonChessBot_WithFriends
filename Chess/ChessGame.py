import sys
import chess
import pygame as pg
import pygame.display

#======= initialize the gameplay window and basic Vars ========#
pg.init()
WIDTH, HEIGHT = 700, 700
screen = pg.display.set_mode((1200, HEIGHT))
pygame.display.set_caption("Chess Bot")
FPS = 24
font = pg.font.SysFont("arial", 20, True)
large_font = pg.font.SysFont("arial", 35, True)
information_surface = pg.Surface((400, 800))
information_surface.fill((0, 0, 0)) # information background color. If not set, it's default is black

red_surface = pg.Surface((200, 100))
red_surface.fill((255, 0, 0))
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
#To hold the .Rect of each promo
promotion_rects = {}

#Logic
selected_square = None
game_over = False
board = chess.Board() #This sets a board with the appropriate setup
gameRunning = True

#ENUM type for game mode with defaults
GAME_PLAYING = 0
GAME_PROMOTION = 1
game_state = GAME_PLAYING
pending_move = None

#Colors for players and board
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SQUARE_COLORS = ((255, 255, 255), (50, 50, 50)) #For the board squares

#Make board
def draw_board():
    for row in range(8):
        for col in range(8):
            color = SQUARE_COLORS[(row + col) % 2]
            pg.draw.rect(screen, color, pg.Rect(col * (WIDTH/8), row * (HEIGHT/8), WIDTH/8, HEIGHT/8))


#Update the pieces and the board
def draw_pieces(main_screen, board_state):
    for square in chess.SQUARES:
        piece = board_state.piece_at(square)
        if piece:

            file_index = chess.square_file(square)
            rank_index = 7 - chess.square_rank(square) # Pygame y-axis is top down
            main_screen.blit(PIECE_IMAGES[piece.symbol()], (file_index * (WIDTH/8), rank_index * (HEIGHT/8)))

#Get the piece when you click
def mouse_to_square(position):
    #Add mouse click logic
    x, y = position
    file = int(x // (WIDTH / 8))
    rank = 7 - int(y // (HEIGHT / 8))
    return chess.square(file, rank)

#Highlight the square selected
def draw_selected_square(square):
    if square is None:
        return
    file = chess.square_file(square)
    rank = 7 - chess.square_rank(square)

    highlight = pg.Surface((WIDTH/8, HEIGHT/8), pygame.SRCALPHA)
    highlight.fill((255, 255, 0, 100))
    screen.blit(highlight, (file * (WIDTH/8), rank * (HEIGHT/8)))

#Show whos turn it is
def draw_turn(turn):
    turn_surface = large_font.render("Turn: " + str(turn), True, WHITE)
    textX = (950 - (turn_surface.get_width() / 2))
    textY = 10
    screen.blit(turn_surface, (textX, textY))

#Right side information box
def draw_information():
    black_box = pg.Rect(800, 0, 400, 800)
    screen.blit(information_surface, black_box)

    #Draw quit button
    size_x = 200
    size_y = 50
    pos_x = 900
    pos_y = 500

    quit_rect = pg.Rect(pos_x, pos_y, size_x, size_y)
    screen.blit(red_surface, quit_rect)

#Ask to promote
def draw_promotion():
    # Draw the options
    promo_text = font.render("Choose a promotion", True, WHITE)
    screen.blit(promo_text, (950 - (promo_text.get_width() / 2), 50))

    #img location and size
    x = 750
    y = 100
    size = 100

    #Draw options
    for key, img in promotion_options.items():
        rect = pg.Rect(x, y, size, size)
        promotion_rects[key] = rect
        screen.blit(img, rect)
        x += size + 10

#========================= GAME LOOP =========================#
while gameRunning:
    if game_state == GAME_PROMOTION:
        draw_promotion()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameRunning = False

        #If you click and its time for a promotion
        if event.type == pg.MOUSEBUTTONDOWN and game_state == GAME_PROMOTION:
            #Promote
            draw_promotion()
            mouseX, mouseY = event.pos

            for piece, rect in promotion_rects.items():
                if rect.collidepoint(mouseX, mouseY):
                    final_move = chess.Move.from_uci(str(pending_move) + piece)
                    board.push(final_move)

                    game_state = GAME_PLAYING
                    pending_move = None
                    promotion_rects.clear()
                    break
            continue

        #If you click and its not game over and also not promotion
        elif event.type == pg.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos
            #If you click other than the board
            if mouseX > WIDTH or mouseY > HEIGHT:
                continue
            square = mouse_to_square(pygame.mouse.get_pos())
            if selected_square is None:
                #First click, select piece
                piece = board.piece_at(square)
                if piece and piece.color == board.turn:
                    selected_square = square
            else:
                #Second click make the move
                move = chess.Move(selected_square, square)
                #is legal
                if move in board.legal_moves:
                    board.push(move)

                    if board.is_game_over():
                        game_over = True
                        print("Game Over: ", board.result())
                else:
                    try:
                        #Check for a promotion move
                        uci_move = chess.Move.from_uci(str(move))
                        for promo in ['q', 'r', 'b', 'n']:
                            if chess.Move.from_uci(str(uci_move) + promo) in board.legal_moves:
                                game_state = GAME_PROMOTION
                                pending_move = uci_move
                                break

                        else:
                            print("Illegal Move")
                    except:
                        print("Except")
                        break

                #Clear selection
                selected_square = None

# ========================= RENDERING =========================== #
    pg.display.flip() #<-- Updates the display
    pg.time.Clock().tick(FPS)
    #Draw the board
    draw_board()
    draw_pieces(screen, board)
    draw_selected_square(selected_square)
    draw_information()
    if board.turn == chess.WHITE:
        current_turn = "White"
    else:
        current_turn = "Black"
    draw_turn(current_turn)