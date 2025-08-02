from Pieces import Pieces
from PiecesMove import PiecesMove
from CheckersBoard import CheckersBoard

class PiecesState:
    points = CheckersBoard.board_points

    previous_red_pieces = None
    previous_white_pieces = None

    evaluation_weights = [8, 6, -6, 8, -8, -4, 4]

    def __init__(self, red, white, is_first):
        if is_first:
            PiecesState.previous_red_pieces = red
            PiecesState.previous_white_pieces = white

        self.current_red_pieces = [self._copy_piece(r) for r in red]
        self.current_white_pieces = [self._copy_piece(w) for w in white]
        self.red_killer = None
        self.white_killer = None
        self.search_depth = 0
        self.evaluation_value = 0

    def _copy_piece(self, p):
        piece = Pieces()
        piece.set_id(p.get_id())
        piece.set_color(p.get_color())
        piece.set_location(p.get_location())
        piece.set_visible(p.is_visible())
        piece.set_king(p.is_king())
        return piece

    def get_value(self):
        red_num = self._get_red_number()
        white_num = self._get_white_number()
        red_kings = self._get_red_king_number()
        white_kings = self._get_white_king_number()
        red_danger = self._get_red_being_killed_number()
        white_danger = self.get_white_being_killed_number()

        if red_num + red_kings == 0:
            return -99999
        if white_num + white_kings == 0:
            return 99999

        return (self.evaluation_weights[0] +
                self.evaluation_weights[1] * red_num +
                self.evaluation_weights[2] * white_num +
                self.evaluation_weights[3] * red_kings +
                self.evaluation_weights[4] * white_kings +
                self.evaluation_weights[5] * red_danger +
                self.evaluation_weights[6] * white_danger)

    def next_states_of_red(self):
        moves = []
        for piece in self.current_red_pieces:
            if piece.is_visible():
                moves.extend(self._next_eating_states(piece, self))
        if not moves:
            for piece in self.current_red_pieces:
                if piece.is_visible():
                    moves.extend(self._next_states(piece, self))
        return moves

    def next_states_of_white(self):
        moves = []
        for piece in self.current_white_pieces:
            if piece.is_visible():
                moves.extend(self._next_eating_states(piece, self))
        if not moves:
            for piece in self.current_white_pieces:
                if piece.is_visible():
                    moves.extend(self._next_states(piece, self))
        return moves

    def _next_eating_states(self, piece, state):
        moves = []
        point = piece.get_location()
        x = point.x // 60 + 1
        y = point.y // 60 + 1
        red = state.current_red_pieces
        white = state.current_white_pieces

        if piece.get_color() == "red":
            if PiecesMove.eat_pieces(piece, state) and piece.is_visible():
                for w in white:
                    if (x - 2 > 0 and y - 2 > 0 and piece.is_king() and w.is_visible() and
                            w.get_location() == self.points[x - 1][y - 1] and
                            self._has_checkers(self.points[x - 2][y - 2]) == "none"):
                        st = PiecesState(red, white, False)
                        st.get_red(self.points[x][y]).set_location(self.points[x - 2][y - 2])
                        st.red_killer = st.get_red(self.points[x - 2][y - 2])
                        st.get_white(self.points[x - 1][y - 1]).set_visible(False)
                        moves.append(st)

                    if (y + 2 < 9 and x - 2 > 0 and w.is_visible() and
                            w.get_location() == self.points[x - 1][y + 1] and
                            self._has_checkers(self.points[x - 2][y + 2]) == "none"):
                        st = PiecesState(red, white, False)
                        st.get_red(self.points[x][y]).set_location(self.points[x - 2][y + 2])
                        st.red_killer = st.get_red(self.points[x - 2][y + 2])
                        st.get_white(self.points[x - 1][y + 1]).set_visible(False)
                        moves.append(st)

                    if (x + 2 < 9 and y - 2 > 0 and piece.is_king() and w.is_visible() and
                            w.get_location() == self.points[x + 1][y - 1] and
                            self._has_checkers(self.points[x + 2][y - 2]) == "none"):
                        st = PiecesState(red, white, False)
                        st.get_red(self.points[x][y]).set_location(self.points[x + 2][y - 2])
                        st.red_killer = st.get_red(self.points[x + 2][y - 2])
                        st.get_white(self.points[x + 1][y - 1]).set_visible(False)
                        moves.append(st)

                    if (x + 2 < 9 and y + 2 < 9 and w.is_visible() and
                            w.get_location() == self.points[x + 1][y + 1] and
                            self._has_checkers(self.points[x + 2][y + 2]) == "none"):
                        st = PiecesState(red, white, False)
                        st.get_red(self.points[x][y]).set_location(self.points[x + 2][y + 2])
                        st.red_killer = st.get_red(self.points[x + 2][y + 2])
                        st.get_white(self.points[x + 1][y + 1]).set_visible(False)
                        moves.append(st)
        else:
            # Similar logic for white pieces (mirroring above with red)
            pass

        return moves

    def _next_states(self, piece, state):
        moves = []
        point = piece.get_location()
        se = PiecesMove.get_south_east_point(point)
        sw = PiecesMove.get_south_west_point(point)
        nw = PiecesMove.get_north_west_point(point)
        ne = PiecesMove.get_north_east_point(point)
        red = state.current_red_pieces
        white = state.current_white_pieces

        if piece.get_color() == "red":
            if se and self._has_checkers(se) == "none":
                st = PiecesState(red, white, False)
                st.get_red(point).set_location(se)
                moves.append(st)
            if sw and self._has_checkers(sw) == "none":
                st = PiecesState(red, white, False)
                st.get_red(point).set_location(sw)
                moves.append(st)
            if ne and self._has_checkers(ne) == "none" and piece.is_king():
                st = PiecesState(red, white, False)
                st.get_red(point).set_location(ne)
                moves.append(st)
            if nw and self._has_checkers(nw) == "none" and piece.is_king():
                st = PiecesState(red, white, False)
                st.get_red(point).set_location(nw)
                moves.append(st)
        else:
            if se and piece.is_king() and self._has_checkers(se) == "none":
                st = PiecesState(red, white, False)
                st.get_white(point).set_location(se)
                moves.append(st)
            if sw and piece.is_king() and self._has_checkers(sw) == "none":
                st = PiecesState(red, white, False)
                st.get_white(point).set_location(sw)
                moves.append(st)
            if ne and self._has_checkers(ne) == "none":
                st = PiecesState(red, white, False)
                st.get_white(point).set_location(ne)
                moves.append(st)
            if nw and self._has_checkers(nw) == "none":
                st = PiecesState(red, white, False)
                st.get_white(point).set_location(nw)
                moves.append(st)
        return moves

    def _get_red_number(self):
        return sum(1 for p in self.current_red_pieces if p.is_visible() and not p.is_king())

    def _get_white_number(self):
        return sum(1 for p in self.current_white_pieces if p.is_visible() and not p.is_king())

    def _get_red_king_number(self):
        return sum(1 for p in self.current_red_pieces if p.is_visible() and p.is_king())

    def _get_white_king_number(self):
        return sum(1 for p in self.current_white_pieces if p.is_visible() and p.is_king())

    def _get_red_being_killed_number(self):
        for p in self.current_red_pieces:
            p.set_counted(False)
        count = 0
        # Mirror the Java nested loop danger detection
        return count

    def get_white_being_killed_number(self):
        for p in self.current_white_pieces:
            p.set_counted(False)
        count = 0
        # Mirror the Java nested loop danger detection
        return count

    def _has_checkers(self, point):
        for p in self.current_red_pieces:
            if p.is_visible() and p.get_location() == point:
                return "red"
        for p in self.current_white_pieces:
            if p.is_visible() and p.get_location() == point:
                return "white"
        return "none"

    def get_white(self, point):
        for p in self.current_white_pieces:
            if p.is_visible() and p.get_location() == point:
                return p
        return None

    def get_red(self, point):
        for p in self.current_red_pieces:
            if p.is_visible() and p.get_location() == point:
                return p
        return None

    def copy(self):
        return PiecesState(self.current_red_pieces, self.current_white_pieces, False)

    def __eq__(self, other):
        if not isinstance(other, PiecesState):
            return False
        for i in range(12):
            cr, orp = self.current_red_pieces[i], other.current_red_pieces[i]
            if cr.get_location() != orp.get_location() or cr.is_visible() != orp.is_visible() or cr.is_king() != orp.is_king():
                return False
            cw, ow = self.current_white_pieces[i], other.current_white_pieces[i]
            if cw.get_location() != ow.get_location() or cw.is_visible() != ow.is_visible() or cw.is_king() != ow.is_king():
                return False
        return True
