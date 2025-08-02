# pieces.py

class Pieces:
    def __init__(self, color=None, id=None):
        self.piece_id = id if id is not None else 0
        self.piece_color = color
        self.is_king_piece = False
        self.is_selected = False
        self.piece_location = (0, 0)  # (x, y)
        self.visible = True
        self.is_counted = False

    # Sets the location using a tuple
    def set_location(self, position):
        if isinstance(position, tuple):
            x, y = position
        else:
            x, y = position.x, position.y
        self.piece_location = (x, y)

        # Promote to king if the piece reaches the opponent's back row
        if self.piece_color == "red" and y // 60 == 7:
            self.is_king_piece = True
        if self.piece_color == "white" and y // 60 == 0:
            self.is_king_piece = True

    # Overloaded version for explicit x, y
    def set_location_xy(self, x, y):
        self.piece_location = (x, y)

        if self.piece_color == "red" and y // 60 == 7:
            self.is_king_piece = True
        if self.piece_color == "white" and y // 60 == 0:
            self.is_king_piece = True

    def get_id(self):
        return self.piece_id

    def set_id(self, id):
        self.piece_id = id

    def get_color(self):
        return self.piece_color

    def set_color(self, color):
        self.piece_color = color

    def is_king(self):
        return self.is_king_piece

    def set_king(self, king):
        self.is_king_piece = king

    def is_selected_piece(self):
        return self.is_selected

    def set_selected(self, selected):
        self.is_selected = selected

    def get_location(self):
        return self.piece_location

    def is_visible(self):
        return self.visible

    def set_visible(self, visible):
        self.visible = visible

    def is_counted_piece(self):
        return self.is_counted

    def set_counted(self, counted):
        self.is_counted = counted

    def __eq__(self, other):
        if not isinstance(other, Pieces):
            return False
        return self.piece_color == other.piece_color and self.piece_id == other.piece_id
