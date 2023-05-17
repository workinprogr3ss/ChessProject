
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

    if piece_type == 'p':  # Pawn
        return get_legal_moves_for_pawn(board, row, col, player)
    elif piece_type == 'r':  # Rook
        return get_legal_moves_for_rook(board, row, col, player)
    elif piece_type == 'n':  # Knight
        return get_legal_moves_for_knight(board, row, col, player)
    elif piece_type == 'b':  # Bishop
        return get_legal_moves_for_bishop(board, row, col, player)
    elif piece_type == 'q':  # Queen
        return get_legal_moves_for_queen(board, row, col, player)
    elif piece_type == 'k':  # King
        return get_legal_moves_for_king(board, row, col, player, has_moved)
    else:
        return []


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


