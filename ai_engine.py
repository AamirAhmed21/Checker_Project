import random

def get_ai_move(board, color):
    # Dummy AI: randomly moves a piece forward if possible
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece and piece.color == color:
                for dcol in [-1, 1]:
                    new_row = row + 1 if color == "dark" else row - 1
                    new_col = col + dcol
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if not board.get_piece(new_row, new_col):
                            return row, col, new_row, new_col
    return 0, 0, 0, 0  # fallback
