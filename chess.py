import pygame

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_SIZE = (512, 512)
screen = pygame.display.set_mode(WINDOW_SIZE)

# Define the colors of the chessboard
white_square_color = (240, 217, 181)
black_square_color = (181, 136, 99)

# Define the initial state of the game board
board = [[('rb', False), ('nb', False), ('bb', False), ('qb', False), ('kb', False), ('bb', False), ('nb', False),
          ('rb', False)],
         [('pb', False), ('pb', False), ('pb', False), ('pb', False), ('pb', False), ('pb', False), ('pb', False),
          ('pb', False)],
         [('  ', None), ('  ', None), ('  ', None), ('  ', None), ('  ', None), ('  ', None), ('  ', None),
          ('  ', None)],
         [('  ', None), ('  ', None), ('  ', None), ('  ', None), ('  ', None), ('  ', None), ('  ', None),
          ('  ', None)],
         [('  ', None), ('  ', None), ('  ', None), ('  ', None), ('  ', None), ('  ', None), ('  ', None),
          ('  ', None)],
         [('  ', None), ('  ', None), ('  ', None), ('  ', None), ('  ', None), ('  ', None), ('  ', None),
          ('  ', None)],
         [('pw', False), ('pw', False), ('pw', False), ('pw', False), ('pw', False), ('pw', False), ('pw', False),
          ('pw', False)],
         [('rw', False), ('nw', False), ('bw', False), ('qw', False), ('kw', False), ('bw', False), ('nw', False),
          ('rw', False)]
         ]

# Define the size of the squares on the chessboard
square_size = WINDOW_SIZE[0] // 8

# Keep track of the selected piece and the position of the mouse
selected_piece = None
mouse_pos = None


def get_legal_moves(board, row, col):
    """
        Given the current state of the board and the position of a piece, returns a list of all legal moves for that piece.

        :param board: the current state of the game board
        :param row: the row of the piece
        :param col: the column of the piece
        :return: a list of legal move positions
    """
    piece, has_moved = board[row][col]
    piece_type = piece[0].lower()
    player = piece[1].lower()

    if piece_type == 'p':
        return get_legal_moves_for_pawn(board, row, col, player)
    elif piece_type == 'r':
        return get_legal_moves_for_rook(board, row, col, player)
    elif piece_type == 'n':  # Knight
        return get_legal_moves_for_knight(board, row, col, player)
    elif piece_type == 'b':
        return get_legal_moves_for_bishop(board, row, col, player)
    elif piece_type == 'q':
        return get_legal_moves_for_queen(board, row, col, player)
    elif piece_type == 'k':
        return get_legal_moves_for_king(board, row, col, player, has_moved)
    else:
        return []


def get_legal_moves_for_pawn(board, row, col, player):
    """
        Get the legal moves for a pawn on the given board at the specified position.

        :param board: the current state of the board
        :param row: the row of the pawn
        :param col: the column of the pawn
        :param player: the player who owns the pawn ('w' for white, 'b' for black)
        :return: a list of legal moves for the pawn
    """
    legal_moves = []
    if player == 'w':
        # White pawn can move one or two spaces forward if it hasn't moved yet
        if row == 6 and board[row - 1][col][0] == '  ' and board[row - 2][col][0] == '  ':
            legal_moves.append((row - 2, col))
        if row > 0 and board[row - 1][col][0] == '  ':
            legal_moves.append((row - 1, col))
        # White pawn can capture diagonally if there is an opponent piece
        if row > 0 and col > 0 and board[row - 1][col - 1][0].islower():
            legal_moves.append((row - 1, col - 1))
        if row > 0 and col < 7 and board[row - 1][col + 1][0].islower():
            legal_moves.append((row - 1, col + 1))
    else:
        # Black pawn can move one or two spaces forward if it hasn't moved yet
        if row == 1 and board[row + 1][col][0] == '  ' and board[row + 2][col][0] == '  ':
            legal_moves.append((row + 2, col))
        if row < 7 and board[row + 1][col][0] == '  ':
            legal_moves.append((row + 1, col))
        # Black pawn can capture diagonally if there is an opponent piece
        if row < 7 and col > 0 and board[row + 1][col - 1][0].isupper():
            legal_moves.append((row + 1, col - 1))
        if row < 7 and col < 7 and board[row + 1][col + 1][0].isupper():
            legal_moves.append((row + 1, col + 1))
    return legal_moves


def get_legal_moves_for_rook(board, row, col, player):
    """
        Get the legal moves for a rook at the specified position.

        :param board: the current state of the board
        :param row: the row of the rook
        :param col: the column of the rook
        :param player: the player whose turn it is ('w' or 'b')
        :return: a list of legal moves as (row, col) tuples
    """
    legal_moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dr, dc in directions:
        for i in range(1, 8):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = board[r][c][0]
                if target_piece == '  ':
                    legal_moves.append((r, c))
                elif (player == 'w' and target_piece.islower()) or (player == 'b' and target_piece.isupper()):
                    legal_moves.append((r, c))
                    break
                else:
                    break
            else:
                break

    return legal_moves


def get_legal_moves_for_knight(board, row, col, player):
    """
        Get the legal moves for a knight at the specified position.

        :param board: the current state of the board
        :param row: the row of the knight
        :param col: the column of the knight
        :param player: the player whose turn it is ('w' or 'b')
        :return: a list of legal moves as (row, col) tuples
    """
    legal_moves = []
    offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    for dr, dc in offsets:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            target_piece = board[r][c][0]
            if target_piece == '  ' or (player == 'w' and target_piece.islower()) or (
                    player == 'b' and target_piece.isupper()):
                legal_moves.append((r, c))

    return legal_moves


def get_legal_moves_for_bishop(board, row, col, player):
    """
        Get the legal moves for a bishop on the given board at the specified position.

        :param board: the current state of the board
        :param row: the row of the bishop
        :param col: the column of the bishop
        :param player: the player who owns the bishop ('w' for white, 'b' for black)
        :return: a list of legal moves for the bishop
    """
    legal_moves = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dr, dc in directions:
        for i in range(1, 8):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = board[r][c][0]
                if target_piece == '  ':
                    legal_moves.append((r, c))
                elif (player == 'w' and target_piece.islower()) or (player == 'b' and target_piece.isupper()):
                    legal_moves.append((r, c))
                    break
                else:
                    break
            else:
                break

    return legal_moves


def get_legal_moves_for_queen(board, row, col, player):
    """
        Given the current state of the board, the row and column of the queen, and the color of the player,
        return a list of legal moves for the queen.

        :param board: the current state of the board
        :param row: the row of the queen
        :param col: the column of the queen
        :param player: the color of the player
        :return: a list of legal moves for the queen
    """
    return get_legal_moves_for_rook(board, row, col, player) + get_legal_moves_for_bishop(board, row, col, player)


def get_legal_moves_for_king(board, row, col, player, has_moved):
    """
        Given the current state of the board, the row and column of the king, the color of the player, and
        a flag indicating whether the king has moved before, return a list of legal moves for the king.

        :param board: the current state of the board
        :param row: the row of the king
        :param col: the column of the king
        :param player: the color of the player
        :param has_moved: a flag indicating whether the king has moved before
        :return: a list of legal moves for the king
    """
    legal_moves = []
    offsets = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]

    for dr, dc in offsets:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            target_piece, target_has_moved = board[r][c]
            if target_piece == '  ' or (player == 'w' and target_piece.islower()) or (
                    player == 'b' and target_piece.isupper()):
                legal_moves.append((r, c))

    # Castling
    if not has_moved:
        # King-side castling
        rook_piece, rook_has_moved = board[row][7]
        if rook_piece.lower() == 'r' and not rook_has_moved:
            if board[row][5] == ('  ', None) and board[row][6] == ('  ', None):
                legal_moves.append((row, col + 2))

        # Queen-side castling
        rook_piece, rook_has_moved = board[row][0]
        if rook_piece.lower() == 'r' and not rook_has_moved:
            if board[row][1] == ('  ', None) and board[row][2] == ('  ', None) and board[row][3] == ('  ', None):
                legal_moves.append((row, col - 2))

    return legal_moves


def move_piece(board, src_row, src_col, dest_row, dest_col):
    """
        Move a piece on the board from the source row and column to the destination row and column.

        :param board: the current state of the board
        :param src_row: the row of the source square
        :param src_col: the column of the source square
        :param dest_row: the row of the destination square
        :param dest_col: the column of the destination square
    """
    piece = board[src_row][src_col][0]
    if (dest_row, dest_col) != (src_row, src_col):
        board[dest_row][dest_col][0] = piece
        board[src_row][src_col][0] = ' '


def draw_board(board, screen, legal_moves):
    """
        Draw the current state of the chess board to the console.

        :param board: a list of lists representing the current state of the board
        :param screen: the Pygame display to draw the board on
        :param legal_moves: a list of legal moves a (row, col) tuples
        :return: None
    """
    for row in range(8):
        for col in range(8):
            color = white_square_color if (row + col) % 2 == 0 else black_square_color
            pygame.draw.rect(screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

            piece, has_moved = board[row][col]
            if piece != '  ':
                piece_image = pygame.image.load(f"images/{piece.lower()}.png")
                piece_image = pygame.transform.scale(piece_image, (square_size, square_size))
                screen.blit(piece_image, (col * square_size, row * square_size))

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


# Run the game loop
running = True
legal_moves = []
while running:

    draw_board(board, screen, legal_moves)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # If the left mouse button is pressed, select the piece or move it
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                row = mouse_pos[1] // square_size
                col = mouse_pos[0] // square_size
                piece, has_moved = board[row][col]
                if selected_piece is None:
                    if piece != '  ':
                        selected_piece = (row, col)
                        legal_moves = get_legal_moves(board, row, col)
                else:
                    src_row, src_col = selected_piece
                    src_piece, src_has_moved = board[src_row][src_col]
                    dest_row, dest_col = row, col
                    if (dest_row, dest_col) != selected_piece and (dest_row, dest_col) in legal_moves:
                        board[dest_row][dest_col] = (src_piece, True)  # Set the moved flag to True
                        board[src_row][src_col] = ('  ', None)
                        # Handle castling moves
                        if src_piece.lower() == 'k' and abs(dest_col - src_col) == 2:
                            if dest_col > src_col:  # King-side castling
                                rook_piece, rook_has_moved = board[src_row][7]
                                board[src_row][5] = (rook_piece, True)
                                board[src_row][7] = ('  ', None)
                            else:  # Queen-side castling
                                rook_piece, rook_has_moved = board[src_row][0]
                                board[src_row][3] = (rook_piece, True)
                                board[src_row][0] = ('  ', None)
                    selected_piece = None
                    legal_moves = []

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()