# pieces_move.py

from Pieces import Pieces

class PiecesMove:
    # Define board points directly to avoid circular import
    board_points = [[None for _ in range(9)] for _ in range(9)]
    has_winner = False
    
    @classmethod
    def init_board_points(cls):
        for i in range(1, 9):
            for j in range(1, 9):
                cls.board_points[i][j] = (60 * (i - 1), 60 * (j - 1))

    @staticmethod
    def get_north_west_point(current_position):
        x_coordinate = 0
        y_coordinate = 0

        for row in range(1, 9):
            for col in range(1, 9):
                if PiecesMove.board_points[row][col] == current_position:
                    x_coordinate = row
                    y_coordinate = col

        if x_coordinate - 1 > 0 and y_coordinate - 1 > 0:
            return PiecesMove.board_points[x_coordinate - 1][y_coordinate - 1]
        return None

    @staticmethod
    def get_north_east_point(current_position):
        x_coordinate = 0
        y_coordinate = 0

        for row in range(1, 9):
            for col in range(1, 9):
                if PiecesMove.board_points[row][col] == current_position:
                    x_coordinate = row
                    y_coordinate = col

        if x_coordinate + 1 < 9 and y_coordinate - 1 > 0:
            return PiecesMove.board_points[x_coordinate + 1][y_coordinate - 1]
        return None

    @staticmethod
    def get_south_west_point(current_position):
        x_coordinate = 0
        y_coordinate = 0

        for row in range(1, 9):
            for col in range(1, 9):
                if PiecesMove.board_points[row][col] == current_position:
                    x_coordinate = row
                    y_coordinate = col

        if x_coordinate - 1 > 0 and y_coordinate + 1 < 9:
            return PiecesMove.board_points[x_coordinate - 1][y_coordinate + 1]
        return None

    @staticmethod
    def get_south_east_point(current_position):
        x_coordinate = 0
        y_coordinate = 0

        for row in range(1, 9):
            for col in range(1, 9):
                if PiecesMove.board_points[row][col] == current_position:
                    x_coordinate = row
                    y_coordinate = col

        if x_coordinate + 1 < 9 and y_coordinate + 1 < 9:
            return PiecesMove.board_points[x_coordinate + 1][y_coordinate + 1]
        return None

    @staticmethod
    def eat_pieces(monster, pieces_state):
        red = pieces_state.current_red_pieces
        white = pieces_state.current_white_pieces
        return PiecesMove.eat_pieces_with_arrays(monster, red, white)

    @staticmethod
    def eat_pieces_with_arrays(monster, red, white):
        x = 0
        y = 0
        if monster is None:
            return False

        for i in range(1, 9):
            for j in range(1, 9):
                if PiecesMove.board_points[i][j] == monster.get_location():
                    x = i
                    y = j

        if monster.color == "red":
            for t in range(12):
                if (x - 2 > 0 and y - 2 > 0 and monster.is_king() and 
                    white[t].is_visible() and 
                    white[t].get_location() == PiecesMove.board_points[x - 1][y - 1] and 
                    PiecesMove.has_pieces(red, white, PiecesMove.board_points[x - 2][y - 2]) == "none"):
                    return True

                if (x - 2 > 0 and y + 2 < 9 and 
                    white[t].get_location() == PiecesMove.board_points[x - 1][y + 1] and 
                    white[t].is_visible() and 
                    PiecesMove.has_pieces(red, white, PiecesMove.board_points[x - 2][y + 2]) == "none"):
                    return True

                if (x + 2 < 9 and y - 2 > 0 and monster.is_king() and 
                    white[t].is_visible() and 
                    white[t].get_location() == PiecesMove.board_points[x + 1][y - 1] and 
                    PiecesMove.has_pieces(red, white, PiecesMove.board_points[x + 2][y - 2]) == "none"):
                    return True

                if (x + 2 < 9 and y + 2 < 9 and 
                    white[t].is_visible() and 
                    white[t].get_location() == PiecesMove.board_points[x + 1][y + 1] and 
                    PiecesMove.has_pieces(red, white, PiecesMove.board_points[x + 2][y + 2]) == "none"):
                    return True
            return False
        else:
            for t in range(12):
                if (x - 2 > 0 and y - 2 > 0 and 
                    red[t].is_visible() and 
                    red[t].get_location() == PiecesMove.board_points[x - 1][y - 1] and 
                    PiecesMove.has_pieces(red, white, PiecesMove.board_points[x - 2][y - 2]) == "none"):
                    return True

                if (x - 2 > 0 and y + 2 < 9 and monster.is_king() and 
                    red[t].get_location() == PiecesMove.board_points[x - 1][y + 1] and 
                    red[t].is_visible() and 
                    PiecesMove.has_pieces(red, white, PiecesMove.board_points[x - 2][y + 2]) == "none"):
                    return True

                if (x + 2 < 9 and y - 2 > 0 and 
                    red[t].is_visible() and 
                    red[t].get_location() == PiecesMove.board_points[x + 1][y - 1] and 
                    PiecesMove.has_pieces(red, white, PiecesMove.board_points[x + 2][y - 2]) == "none"):
                    return True

                if (x + 2 < 9 and y + 2 < 9 and monster.is_king() and 
                    red[t].is_visible() and 
                    red[t].get_location() == PiecesMove.board_points[x + 1][y + 1] and 
                    PiecesMove.has_pieces(red, white, PiecesMove.board_points[x + 2][y + 2]) == "none"):
                    return True
            return False

    @staticmethod
    def has_pieces(red, white, point):
        for i in range(12):
            if red[i].is_visible() and red[i].get_location() == point:
                return "red"
            if white[i].is_visible() and white[i].get_location() == point:
                return "white"
        return "none"

    @staticmethod
    def has_pieces_state(pieces_state, point):
        red = pieces_state.current_red_pieces
        white = pieces_state.current_white_pieces
        return PiecesMove.has_pieces(red, white, point)
