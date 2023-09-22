import pygame
import sys
from board import Board
from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King


class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.WINDOW_SIZE = (712, 512)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)

        # Initialize game variables
        self.square_size = self.WINDOW_SIZE[0] // 8
        self.selected_piece = None
        self.selected_position = None
        self.board = Board(self.screen)
        self.turn = "white"  # white goes first
        self.captured_pieces = {"w": [], "b": []}

        # Initialize game and time settings
        self.max_turn_time = 600  # 10 minutes
        self.white_total_time = self.max_turn_time
        self.white_start_time = None
        self.black_total_time = self.max_turn_time
        self.black_start_time = None

        self.font = pygame.font.Font(None, 36)  # Adjust the font size as necessary

        
    def game_loop(self):
        """Main game loop"""
        # Initialize game loop variables
        running = True
        legal_moves = []
        
        self.white_start_time = pygame.time.get_ticks()  # initialize white start time
        
        while running:
            self.board.draw_board(self.screen, self.selected_position, legal_moves)

            self.update_timer()
            self.draw_timer()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        board_size = 512
                        row = mouse_pos[1] // (board_size // 8)
                        col = mouse_pos[0] // (board_size // 8)
                        piece = self.board.board[row][
                            col
                        ]  # Not really piece but selected square on the board

                        # If no piece is selected, then select the piece
                        if self.selected_piece is None:
                            if piece is not None:
                                # Prevents players to select opponents pieces
                                wrong_piece_white = (
                                    piece.color == "b" and self.turn == "white"
                                )
                                wrong_piece_black = (
                                    piece.color == "w" and self.turn == "black"
                                )
                                # If player selects the wrong piece, then reset the selection
                                if wrong_piece_black or wrong_piece_white:
                                    break

                                # If player selects the right piece, then select the piece
                                self.selected_piece = piece
                                self.selected_position = (row, col)
                                legal_moves = piece.get_legal_moves(
                                    self.selected_position, self.board
                                )

                                # If selected piece has no legal moves, then reset the selection (basically not allowing player to select the piece)
                                if legal_moves == []:
                                    self.selected_piece = None
                                    self.selected_position = None

                        # If a piece is selected, then select the destination
                        else:
                            dest_pos = (row, col)
                            
                            # If player selects the same piece, then reset the selection
                            if dest_pos == self.selected_position:
                                self.selected_piece = None
                                self.selected_position = None
                                legal_moves = []

                            # If player selects a legal move, then move the piece
                            elif dest_pos in legal_moves:
                                # Castling
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

                                # Pawn promotion, #####need to implement en passant#####
                                elif isinstance(self.selected_piece, Pawn):
                                    self.selected_piece.has_moved = True
                                    color = self.selected_piece.color
                                    self.move_piece(row, col)
                                    legal_moves = []
                                    if dest_pos[0] == 0 or dest_pos[0] == 7:
                                        self.board.board[row][col] = Queen(color)

                                # If not King or Pawn, then move the piece
                                else:
                                    self.move_piece(row, col)
                                    legal_moves = []

            
            running = self.check_for_time_up()
            self.draw_timer()
            #self.draw_captured_pieces()
            pygame.display.flip()

        pygame.quit()

    def move_piece(self, row, col):
        # Check for captured piece
        captured_piece = self.board.board[row][col]
        if captured_piece is not None:
            self.captured_pieces[captured_piece.color].append(captured_piece)
        """Moves the piece on the board"""
        self.board.board[row][col] = self.selected_piece  # Moves piece on board
        self.board.board[self.selected_position[0]][
            self.selected_position[1]
        ] = None  # Sets old position of piece to None
        # self.selected_piece.position = dest_pos
        self.selected_piece = None
        self.selected_position = None
        self.switch_turns()

    def switch_turns(self):
        """Updates time and switches turns"""
        
        # Existing logic to switch turn
        self.turn = "black" if self.turn == "white" else "white"

        # Add logic to update total time and reset start time
        if self.turn == "white":
            self.black_total_time -= (pygame.time.get_ticks() - self.black_start_time) / 1000  # Update black's total time
            self.white_start_time = pygame.time.get_ticks()  # Reset white's start time
        else:
            self.white_total_time -= (pygame.time.get_ticks() - self.white_start_time) / 1000  # Update white's total time
            self.black_start_time = pygame.time.get_ticks()  # Reset black's start time
        

    def check_for_time_up(self):
        # Check if time's up
        if self.white_total_time <= 0:
            print("White's time is up!")
            # Add logic to display this message on the screen
            return False
        elif self.black_total_time <= 0:
            print("Black's time is up!")
            # Add logic to display this message on the screen
            return False
        return True
    
    def draw_timer(self):
        # Calculate remaining time in seconds
        if self.turn == "white":
            elapsed_time = (pygame.time.get_ticks() - self.white_start_time) / 1000
            remaining_time = max(0, self.white_total_time - elapsed_time)
        else:
            elapsed_time = (pygame.time.get_ticks() - self.black_start_time) / 1000
            remaining_time = max(0, self.black_total_time - elapsed_time)

        # Convert remaining time to a string
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        time_string = f"{minutes}:{seconds:02}"

        # Render the time strings to surfaces
        white_time_string = f"{int(self.white_total_time // 60)}:{int(self.white_total_time % 60):02}"
        black_time_string = f"{int(self.black_total_time // 60)}:{int(self.black_total_time % 60):02}"
        white_text = self.font.render(white_time_string, True, (0, 0, 0))
        black_text = self.font.render(black_time_string, True, (0, 0, 0))

        # Draw rectangles to cover the previous texts
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(562, 452, 100, 50))  # For white timer
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(562, 10, 100, 50))  # For black timer

        # Draw the text surfaces on the screen at certain positions
        self.screen.blit(white_text, (587, 462))  # For white timer
        self.screen.blit(black_text, (587, 20))  # For black timer

    def update_timer(self):
        current_time = pygame.time.get_ticks()

        if self.turn == "white":
            elapsed_time = (current_time - self.white_start_time) / 1000  # Time elapsed in seconds
            self.white_total_time = max(0, self.white_total_time - elapsed_time)
            self.white_start_time = current_time  # Reset the start time for the next frame
        else:
            elapsed_time = (current_time - self.black_start_time) / 1000  # Time elapsed in seconds
            self.black_total_time = max(0, self.black_total_time - elapsed_time)
            self.black_start_time = current_time  # Reset the start time for the next frame


    def draw_captured_pieces(self):
        # Set starting position for captured pieces
        x, y = 530, 50

        # Draw a light gray rectangle behind the captured pieces
        pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(x, y, 170, self.WINDOW_SIZE[1]-y))

        # Loop through each list of captured pieces
        for color in ["w", "b"]:
            for piece in self.captured_pieces[color]:
                # Draw the piece at the current position
                self.screen.blit(piece.image, (x, y))

                # Move the position to the right for the next piece
                x += piece.image.get_width() + 10

                # If the position is too far to the right, move it back to the left and down a row
                if x > self.WINDOW_SIZE[0] - piece.image.get_width():
                    x = 10
                    y += piece.image.get_height() + 10


if __name__ == "__main__":
    game = Game()
    game.game_loop()
