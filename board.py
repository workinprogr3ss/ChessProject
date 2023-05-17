from pieces import Pawn, Rook, Knight, Bishop, Queen, King
import pygame

# Define the colors of the chessboard
white_square_color = (240, 217, 181)
black_square_color = (181, 136, 99)

# Define the size of the squares on the chessboard
WINDOW_SIZE = (512, 512)
square_size = WINDOW_SIZE[0] // 8


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.selected_piece = None
        self.legal_moves = []
        self.board = self.initialize_board()

    def initialize_board(self):
        # Define the initial state of the game board
        board = [[Rook('b'), Knight('b'), Bishop('b'), Queen('b'), King('b'), Bishop('b'), Knight('b'), Rook('b')],
                 [Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b')],
                 [None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None],
                 [None, None, None, None, None, None, None, None],
                 [Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w')],
                 [Rook('w'), Knight('w'), Bishop('w'), Queen('w'), King('w'), Bishop('w'), Knight('w'), Rook('w')]
                 ]
        return board

    def draw_board(self, screen, selected_piece, legal_moves):
        # Draw the squares
        for row in range(8):
            for col in range(8):
                color = white_square_color if (row + col) % 2 == 0 else black_square_color
                pygame.draw.rect(screen, color,
                                 pygame.Rect(col * square_size, row * square_size, square_size, square_size))

        # Draw the pieces
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    screen.blit(piece.image, (col * square_size, row * square_size))

        # If a piece is selected, draw a circle around it
        if selected_piece is not None:
            row, col = selected_piece
            pygame.draw.circle(screen, (255, 0, 0), ((col + 0.5) * square_size, (row + 0.5) * square_size),
                               square_size // 3)

        # Draw legal move indicators for the selected piece
        if legal_moves:
            for r, c in legal_moves:
                pygame.draw.circle(screen, (0, 255, 0), ((c + 0.5) * square_size, (r + 0.5) * square_size),
                                   square_size // 10)

        pygame.display.flip()
