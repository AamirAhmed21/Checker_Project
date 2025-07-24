from piece import Piece

ROWS, COLS = 8, 8

class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        board[row][col] = Piece(row, col, "dark")
                    elif row > 4:
                        board[row][col] = Piece(row, col, "light")
        return board

    def move(self, piece, to_row, to_col):
        self.board[piece.row][piece.col] = None
        piece.row, piece.col = to_row, to_col
        self.board[to_row][to_col] = piece
        # Kinging
        if (piece.color == "dark" and to_row == ROWS - 1) or (piece.color == "light" and to_row == 0):
            piece.make_king()

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = None

    def get_piece(self, row, col):
        return self.board[row][col]

    def print_board(self):
        for row in self.board:
            print(" ".join(str(p) if p else "." for p in row))

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece and piece.color == color:
                    pieces.append(piece)
        return pieces

    def get_valid_moves(self, piece):
        moves = {}
        for dr, dc in piece.directions():
            row, col = piece.row + dr, piece.col + dc
            if 0 <= row < ROWS and 0 <= col < COLS:
                target = self.get_piece(row, col)
                if not target:
                    moves[(row, col)] = []  # normal move
                elif target.color != piece.color:
                    # Check jump
                    jump_row, jump_col = row + dr, col + dc
                    if 0 <= jump_row < ROWS and 0 <= jump_col < COLS and not self.get_piece(jump_row, jump_col):
                        moves[(jump_row, jump_col)] = [(row, col)]  # capture move
        return moves

    def get_all_valid_moves(self, color):
        all_moves = {}
        for piece in self.get_all_pieces(color):
            moves = self.get_valid_moves(piece)
            if moves:
                all_moves[piece] = moves
        return all_moves