import pygame

# Define the size of the squares on the chessboard
WINDOW_SIZE = (512, 512)
square_size = WINDOW_SIZE[0] // 8


class Piece:
    def __init__(self, color):
        self.color = color
        self.image = None
        self.has_moved = False

    def load_image(self, name):
        self.image = pygame.image.load(f"images/{name}.png")
        self.image = pygame.transform.scale(self.image, (square_size, square_size))


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.load_image(f"p{color}")

    def get_legal_moves(self, position, board):
        """
        Get the legal moves for a pawn on the given board at the specified position.
        :param position: the current position of the pawn as (row, col)
        :param board: the current state of the board
        :return: a list of legal moves for the pawn
        """
        row, col = position
        legal_moves = []
        if self.color == 'w':
            # White pawn can move one or two spaces forward if it hasn't moved yet
            if row == 6 and board.board[row - 1][col] is None and board.board[row - 2][col] is None:
                legal_moves.append((row - 2, col))
            if row > 0 and board.board[row - 1][col] is None:
                legal_moves.append((row - 1, col))
            # White pawn can capture diagonally if there is an opponent piece
            if row > 0 and col > 0 and board.board[row - 1][col - 1] and board.board[row - 1][col - 1].color == 'b':
                legal_moves.append((row - 1, col - 1))
            if row > 0 and col < 7 and board.board[row - 1][col + 1] and board.board[row - 1][col + 1].color == 'b':
                legal_moves.append((row - 1, col + 1))
        elif self.color == 'b':
            # Black pawn can move one or two spaces forward if it hasn't moved yet
            if row == 1 and board.board[row + 1][col] is None and board.board[row + 2][col] is None:
                legal_moves.append((row + 2, col))
            if row < 7 and board.board[row + 1][col] is None:
                legal_moves.append((row + 1, col))
            # Black pawn can capture diagonally if there is an opponent piece
            if row < 7 and col > 0 and board.board[row + 1][col - 1] and board.board[row + 1][col - 1].color == 'w':
                legal_moves.append((row + 1, col - 1))
            if row < 7 and col < 7 and board.board[row + 1][col + 1] and board.board[row + 1][col + 1].color == 'w':
                legal_moves.append((row + 1, col + 1))
        return legal_moves


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.load_image(f"r{color}")

    def get_legal_moves(self, position, board):
        """
        Get the legal moves for a rook at the specified position.
        :param position: the current position of the rook as (row, col)
        :param board: the current state of the board
        :return: a list of legal moves as (row, col) tuples
        """
        row, col = position
        legal_moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            for i in range(1, 8):
                r, c = row + dr * i, col + dc * i
                if 0 <= r < 8 and 0 <= c < 8:
                    target_piece = board.board[r][c]
                    if target_piece is None:
                        legal_moves.append((r, c))
                    elif target_piece.color != self.color:
                        legal_moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break

        return legal_moves


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.load_image(f"n{color}")

    def get_legal_moves(self, position, board):
        """
        Get the legal moves for a knight at the specified position.
        :param position: the current position of the knight as (row, col)
        :param board: the current state of the board
        :return: a list of legal moves as (row, col) tuples
        """
        row, col = position
        legal_moves = []
        offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for dr, dc in offsets:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = board.board[r][c]
                if target_piece is None or target_piece.color != self.color:
                    legal_moves.append((r, c))

        return legal_moves


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.load_image(f"b{color}")

    def get_legal_moves(self, position, board):
        """
        Get the legal moves for a bishop at the specified position.
        :param position: the current position of the bishop as (row, col)
        :param board: the current state of the board
        :return: a list of legal moves as (row, col) tuples
        """
        row, col = position
        legal_moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            for i in range(1, 8):
                r, c = row + dr * i, col + dc * i
                if 0 <= r < 8 and 0 <= c < 8:
                    target_piece = board.board[r][c]
                    if target_piece is None:
                        legal_moves.append((r, c))
                    elif target_piece.color != self.color:
                        legal_moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break

        return legal_moves


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.load_image(f"q{color}")

    def get_legal_moves(self, position, board):
        """
        Get the legal moves for a queen at the specified position.
        :param position: the current position of the queen as (row, col)
        :param board: the current state of the board
        :return: a list of legal moves as (row, col) tuples
        """
        # Combine the moves of a bishop and rook, since a queen can move like both
        return Bishop(self.color).get_legal_moves(position, board) + Rook(self.color).get_legal_moves(position, board)


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.load_image(f"k{color}")
        self.has_moved = False

    def get_legal_moves(self, position, board):
        """
        Get the legal moves for a king at the specified position.
        :param position: the current position of the king as (row, col)
        :param board: the current state of the board
        :return: a list of legal moves as (row, col) tuples
        """
        row, col = position
        legal_moves = []
        offsets = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]

        for dr, dc in offsets:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = board.board[r][c]
                if target_piece is None or target_piece.color != self.color:
                    legal_moves.append((r, c))

        # Castling
        if not self.has_moved:
            # King-side castling
            rook_piece = board.board[row][7]
            if isinstance(rook_piece, Rook) and not rook_piece.has_moved:
                if board.board[row][5] is None and board.board[row][6] is None:
                    legal_moves.append((row, col + 2))

            # Queen-side castling
            rook_piece = board.board[row][0]
            if isinstance(rook_piece, Rook) and not rook_piece.has_moved:
                if all(board.board[row][i] is None for i in range(1, 4)):
                    legal_moves.append((row, col - 2))

        return legal_moves
