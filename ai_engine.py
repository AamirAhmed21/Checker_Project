import random 

def get_compeasy_move(board, color):
    valid_moves = board.get_all_valid_moves(color)
    print ("avalible moves:", valid_moves)
    if not valid_moves: #player lose a turn if no moves possible
        print("no  moves founds, skipping turn...")
        return None
    
    easy_moves = []
    for piece, moves in valid_moves.items():
        for final_pos, captured in moves.items():
            original_row, original_col = piece.row, piece.col
            final_row, final_col = final_pos
            easy_moves.append((original_row, original_col, final_row, final_col))
    return random.choice(easy_moves)    
    

def get_compmedium_move(board, color):    
    valid_moves = board.get_all_valid_moves(color) 
    print ("avalible  moves:", valid_moves)

    if not valid_moves: #Player lose a turn if no moves possible
        print("no  moves founds, skipping turn...")
        return None
        
    capture_moves = [] 
    noncapture_moves = [] 

    for piece, moves in valid_moves.items(): #loops for each piece and each of that pieces valid moves
        for final_pos, captured in moves.items():
            original_row, original_col = piece.row, piece.col
            final_row, final_col = final_pos

            if captured: #stores the amount of pieces captured for a each move
                capture_moves.append((original_row, original_col, final_row, final_col, len(captured)))
            else:
                noncapture_moves.append((original_row, original_col, final_row, final_col))
    if capture_moves: # finds and picks the max captures for a move
        best_captures = max(move[4] for move in capture_moves) 
        best_captures = [move for move in capture_moves if move[4] == best_captures]
        move = random.choice(best_captures)
        return move[:4]
    elif noncapture_moves:
        return random.choice(noncapture_moves)
    else: 
        return None

def get_comphard_move(board, color):
    valid_moves = board.get_all_valid_moves(color) 
    print ("avalible moves:", valid_moves)
    if not valid_moves: #Player  lose a turn if no  moves possible
        print("no moves founds, skipping turn...")
        return None
       
    optimal_move = None 
    best_captures = -1 

    for piece, moves in valid_moves.items(): #loops for each piece and each of that pieces valid moves
        for final_pos, captured in moves.items(): #loops for each piece and each end position for that piece and checks if captures pieces
            original_row, original_col = piece.row, piece.col
            final_row, final_col = final_pos
            if captured:
              current_captures = len(captured) #tracks amount of captures
            if current_captures > best_captures: # check to see if the current amound of captures is the highest this far
                best_captures = current_captures
                optimal_move = (original_row, original_col, final_row, final_col)

            elif optimal_move is None:
              optimal_move = (original_row, original_col, final_row, final_col)
    return optimal_move if optimal_move is not None else None
    

