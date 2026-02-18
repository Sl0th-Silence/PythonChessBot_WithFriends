import chess
import pygame as pg
pg.init() # Need to init before pulling in the other class
#import class
import ChessEngine as cEngine

# This sets a board with the appropriate setup
board = chess.Board()

#USING NEW CLASSES HERE ======================================
chess_game = cEngine.ChessEngine()
chess_game.draw_board()
chess_game.draw_pieces(cEngine.cv.screen, board)

#======= initialize the window name and basic Logic ========#
pg.display.set_caption("Chess Game")

#Logic
game_over = False
gameRunning = True
#========================= GAME LOOP =========================#
while gameRunning:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameRunning = False
        #If you click and it's time for a promotion
        if event.type == pg.MOUSEBUTTONDOWN and chess_game.game_state == chess_game.GAME_PROMOTION:
            mouseX, mouseY = event.pos

            for piece, rect in cEngine.cv.promotion_rects.items():
                if rect.collidepoint(mouseX, mouseY):
                    final_move = chess.Move.from_uci(
                        str(chess_game.pending_move) + piece
                    )
                    board.push(final_move)
                    chess_game.add_move_to_log(final_move)

                    chess_game.game_state = chess_game.GAME_PLAYING
                    chess_game.pending_move = None
                    #cEngine.cv.promotion_rects.clear()
                    break

            continue

        #If you click and its not game over and also not promotion
        elif event.type == pg.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos
            #If you click other than the board
            if mouseX > cEngine.cv.WIDTH or mouseY > cEngine.cv.HEIGHT:
                #We can check for quit button
                if cEngine.cv.quit_rect.collidepoint(mouseX, mouseY):
                    quit(1)
                else:
                    continue
            square = chess_game.mouse_to_square(pg.mouse.get_pos())
            if chess_game.selected_square is None:
                #First click, select piece
                piece = board.piece_at(square)
                if piece and piece.color == board.turn:
                    chess_game.selected_square = square
            else:
                #Second click make the move
                move = chess.Move(chess_game.selected_square, square)
                #is legal
                if move in board.legal_moves:
                    chess_game.add_move_to_log(move)
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
                                chess_game.game_state = chess_game.GAME_PROMOTION
                                chess_game.pending_move = uci_move
                                break
                        else:
                            print("Illegal Move")
                    except:
                        print("Except")
                        break

                #Clear selection
                chess_game.selected_square = None

# ========================= RENDERING =========================== #
    #Draw the board
    chess_game.draw_board()
    chess_game.draw_information()
    chess_game.draw_pieces(cEngine.cv.screen, board)
    chess_game.draw_selected_square(chess_game.selected_square)
    if chess_game.game_state == chess_game.GAME_PROMOTION:
        chess_game.draw_promotion()

    if board.turn == chess.WHITE:
        current_turn = "White"
    else:
        current_turn = "Black"
    chess_game.draw_turn(current_turn)

    # Update UI
    cEngine.cv.ui_manager.update(1 / chess_game.FPS)
    cEngine.cv.ui_manager.draw_ui(cEngine.cv.screen)


    pg.display.flip()
    pg.time.Clock().tick(chess_game.FPS)
