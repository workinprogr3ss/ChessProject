import pygame
from board import Board
from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King


# NOT SURE WHAT ELSE TO ADD HERE
class Game:
    def __init__(self):
        pygame.init()
        self.WINDOW_SIZE = (512, 512)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)

        self.square_size = self.WINDOW_SIZE[0] // 8
        self.selected_piece = None
        self.selected_position = None
        self.board = Board(self.screen)
        self.turn = "white"  # white goes first

    def game_loop(self):
        running = True
        legal_moves = []
        while running:
            self.board.draw_board(self.screen, self.selected_position, legal_moves)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        row = mouse_pos[1] // self.square_size
                        col = mouse_pos[0] // self.square_size
                        piece = self.board.board[row][
                            col
                        ]  # Not really piece but selected square on the board
                        if self.selected_piece is None:
                            if piece is not None:
                                # Turn system by not allowing players to select opponents pieces
                                wrong_piece_white = (
                                    piece.color == "b" and self.turn == "white"
                                )
                                wrong_piece_black = (
                                    piece.color == "w" and self.turn == "black"
                                )
                                if wrong_piece_black or wrong_piece_white:
                                    break
                                self.selected_piece = piece
                                self.selected_position = (row, col)
                                legal_moves = piece.get_legal_moves(
                                    self.selected_position, self.board
                                )
                                # If selected piece has no legal moves, then reset the selection (basically not allowing player to select the piece)
                                if legal_moves == []:
                                    self.selected_piece = None
                                    self.selected_position = None
                        else:
                            dest_pos = (row, col)
                            # If player selects the same piece, then reset the selection
                            if dest_pos == self.selected_position:
                                self.selected_piece = None
                                self.selected_position = None
                                legal_moves = []

                            # If player selects a legal move, then move the piece
                            elif dest_pos in legal_moves:
                                if isinstance(self.selected_piece, King):
                                    self.selected_piece.has_moved = True
                                    self.move_piece(row, col)
                                    legal_moves = []
                                    if dest_pos[1] == 6:
                                        self.board.board[row][5] = self.board.board[
                                            row
                                        ][7]
                                        self.board.board[row][7] = None
                                        self.board.board[row][5].has_moved = True
                                    elif dest_pos[1] == 2:
                                        self.board.board[row][3] = self.board.board[
                                            row
                                        ][0]
                                        self.board.board[row][0] = None
                                        self.board.board[row][3].has_moved = True

                                elif isinstance(self.selected_piece, Pawn):
                                    self.selected_piece.has_moved = True
                                    color = self.selected_piece.color
                                    self.move_piece(row, col)
                                    legal_moves = []
                                    if dest_pos[0] == 0 or dest_pos[0] == 7:
                                        self.board.board[row][col] = Queen(color)

                                else:
                                    self.move_piece(row, col)
                                    legal_moves = []

            pygame.display.flip()

        pygame.quit()

    def checkmate(self):
        """Checks if the game is over"""
        pass

    def move_piece(self, row, col):
        """Moves the piece on the board"""
        self.board.board[row][col] = self.selected_piece  # Moves piece on board
        self.board.board[self.selected_position[0]][
            self.selected_position[1]
        ] = None  # Sets old position of piece to None
        # self.selected_piece.position = dest_pos
        self.selected_piece = None
        self.selected_position = None
        self.turn = "black" if self.turn == "white" else "white"  # switch turns


if __name__ == "__main__":
    game = Game()
    game.game_loop()
