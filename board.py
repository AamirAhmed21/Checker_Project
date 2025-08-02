from piece import Piece

# Constants for board dimensions
ROWS, COLS = 8, 8

class Board:
    def __init__(self): # Intializes the board
        self.board = self.create_board()

    def create_board(self): # creates a 8x8 board and places pieces
        board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        board[row][col] = Piece(row, col, "dark")
                    elif row > 4:
                        board[row][col] = Piece(row, col, "light")
        return board

    def move(self, piece, to_row, to_col): # moves a piece to a new position
        self.board[piece.row][piece.col] = None # removes the pieces previous position
        piece.row, piece.col = to_row, to_col # update piece position   
        self.board[to_row][to_col] = piece # places the piece in its new position
        # Kinging the piece if it reaches the opponents end of the board
        if (piece.color == "dark" and to_row == ROWS - 1) or (piece.color == "light" and to_row == 0):
            piece.make_king()

    def remove(self, pieces): # removes a piece from the board
        for piece in pieces:
            self.board[piece.row][piece.col] = None

    def get_piece(self, row, col):  # returns if there is a piece or not a the coordinates
        return self.board[row][col]

    def print_board(self): # prints a text version of the board
        for row in self.board:
            print(" ".join(str(p) if p else "." for p in row))

    def get_all_pieces(self, color): # returns all piece of the specified color
        pieces = []
        for row in self.board:
            for piece in row:
                if piece and piece.color == color:
                    pieces.append(piece)
        return pieces

    def get_valid_moves(self, piece): # returns all possible moves for a piece
        moves = {}
        for dr, dc in piece.directions():  
            row, col = piece.row + dr, piece.col + dc
            if 0 <= row < ROWS and 0 <= col < COLS: # check if move is within the board
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