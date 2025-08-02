from board import Board
from ai_engine import get_ai_move

class GameManager:
    def __init__(self):
        self.board = Board()
        self.turn = "dark"  # dark starts
        self.running = True

    def start(self):
        while self.running:
            self.board.print_board()
            print(f"\n{self.turn}'s turn")
            if not self.has_moves(self.turn):
                print(f"{self.turn} has no valid moves. Game over!")
                self.running = False
                # Winner/Draw detection
                opponent = "light" if self.turn == "dark" else "dark"
                if self.has_moves(opponent):
                    print(f"{opponent} wins!")
                else:
                    print("It's a draw!")
                break
            if self.turn == "light":
                self.human_move()
            else:
                self.ai_move()
            self.switch_turn()

    def switch_turn(self):
        self.turn = "light" if self.turn == "dark" else "dark"

    def has_moves(self, color):
        return bool(self.board.get_all_valid_moves(color))

    def human_move(self):
        valid_moves = self.board.get_all_valid_moves(self.turn)
        must_capture = self.must_capture(valid_moves)
        while True:
            print("Valid moves:")
            for piece, moves in valid_moves.items():
                for move, captured in moves.items():
                    move_type = "capture" if captured else "move"
                    print(f"Piece at ({piece.row},{piece.col}) can {move_type} to {move}")
            try:
                from_row = int(input("From row: "))
                from_col = int(input("From col: "))
                to_row = int(input("To row: "))
                to_col = int(input("To col: "))
            except ValueError:
                print("Invalid input. Please enter numbers.")
                continue
            piece = self.board.get_piece(from_row, from_col)
            if not piece or piece.color != self.turn:
                print("Invalid piece selection.")
                continue
            moves = valid_moves.get(piece, {})
            if (to_row, to_col) not in moves:
                print("Invalid move.")
                continue
            if must_capture and not moves[(to_row, to_col)]:
                print("You must capture if possible.")
                continue
            # Perform move
            self.board.move(piece, to_row, to_col)
            if moves[(to_row, to_col)]:
                # Remove captured piece(s)
                for pos in moves[(to_row, to_col)]:
                    captured_piece = self.board.get_piece(*pos)
                    if captured_piece:
                        self.board.remove([captured_piece])
                # Check for additional jumps
                while True:
                    new_moves = self.board.get_valid_moves(piece)
                    capture_moves = {k: v for k, v in new_moves.items() if v}
                    if capture_moves:
                        self.board.print_board()
                        print(f"You must continue jumping with piece at ({piece.row},{piece.col})")
                        print("Available jumps:")
                        for move, captured in capture_moves.items():
                            print(f"Jump to {move}")
                        try:
                            to_row = int(input("To row: "))
                            to_col = int(input("To col: "))
                        except ValueError:
                            print("Invalid input. Please enter numbers.")
                            continue
                        if (to_row, to_col) not in capture_moves:
                            print("Invalid jump.")
                            continue
                        self.board.move(piece, to_row, to_col)
                        for pos in capture_moves[(to_row, to_col)]:
                            captured_piece = self.board.get_piece(*pos)
                            if captured_piece:
                                self.board.remove([captured_piece])
                    else:
                        break
            break

    def must_capture(self, valid_moves):
        for moves in valid_moves.values():
            for captured in moves.values():
                if captured:
                    return True
        return False

    def ai_move(self):
        valid_moves = self.board.get_all_valid_moves(self.turn)
        must_capture = self.must_capture(valid_moves)
        # Simple AI: pick the first valid move (prioritize captures)
        for piece, moves in valid_moves.items():
            for move, captured in moves.items():
                if must_capture and not captured:
                    continue
                self.board.move(piece, *move)
                if captured:
                    for pos in captured:
                        captured_piece = self.board.get_piece(*pos)
                        if captured_piece:
                            self.board.remove([captured_piece])
                    # Multiple jumps for AI
                    while True:
                        new_moves = self.board.get_valid_moves(piece)
                        capture_moves = {k: v for k, v in new_moves.items() if v}
                        if capture_moves:
                            next_move = list(capture_moves.keys())[0]
                            self.board.move(piece, *next_move)
                            for pos in capture_moves[next_move]:
                                captured_piece = self.board.get_piece(*pos)
                                if captured_piece:
                                    self.board.remove([captured_piece])
                        else:
                            break
                print(f"AI moved from ({piece.row},{piece.col}) to {move}")
                return
