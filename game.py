import pygame
from board import Board

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
                        piece = self.board.board[row][col]
                        if self.selected_piece is None:
                            if piece is not None:
                                self.selected_piece = piece
                                self.selected_position = (row, col)
                                legal_moves = piece.get_legal_moves(self.board)
                        else:
                            dest_pos = (row, col)
                            if dest_pos in legal_moves:
                                self.board.board[row][col] = self.selected_piece
                                self.board.board[self.selected_position[0]][self.selected_position[1]] = None
                                self.selected_piece.position = dest_pos
                                self.selected_piece = None
                                self.selected_position = None
                                legal_moves = []

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.game_loop()
