class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.is_king = False

    def make_king(self):
        self.is_king = True

    def __repr__(self):
        if self.is_king:
            return f"K-{self.color[0].upper()}"
        else:
            return f"M-{self.color[0].upper()}"

    def directions(self):
        # Returns allowed move directions for this piece
        if self.is_king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return [(1, -1), (1, 1)] if self.color == "dark" else [(-1, -1), (-1, 1)]