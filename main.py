import random
import time

# Chess piece representations
pieces = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}

# Initialize the chess board
def init_board():
    return [
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
    ]

# Print the chess board
def print_board(board):
    print("  a b c d e f g h")
    for i, row in enumerate(board):
        print(f"{8-i} ", end="")
        for piece in row:
            print(pieces.get(piece, ' '), end=" ")
        print(f"{8-i}")
    print("  a b c d e f g h")

# Get all possible moves for a player
def get_possible_moves(board, player, last_move):
    moves = []
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece.isupper() if player == 'white' else piece.islower():
                if piece.lower() == 'p':
                    moves.extend(get_pawn_moves(board, i, j, player, last_move))
                elif piece.lower() == 'r':
                    moves.extend(get_rook_moves(board, i, j, player))
                elif piece.lower() == 'n':
                    moves.extend(get_knight_moves(board, i, j, player))
                elif piece.lower() == 'b':
                    moves.extend(get_bishop_moves(board, i, j, player))
                elif piece.lower() == 'q':
                    moves.extend(get_queen_moves(board, i, j, player))
                elif piece.lower() == 'k':
                    moves.extend(get_king_moves(board, i, j, player))
    return moves

# Helper function to check if a move is within the board
def is_valid_position(i, j):
    return 0 <= i < 8 and 0 <= j < 8

# Get pawn moves (including en passant and promotion)
def get_pawn_moves(board, i, j, player, last_move):
    moves = []
    direction = -1 if player == 'white' else 1
    start_row = 6 if player == 'white' else 1

    # Regular move
    if is_valid_position(i + direction, j) and board[i + direction][j] == ' ':
        moves.append((i, j, i + direction, j))
        # Double move from start position
        if i == start_row and board[i + 2*direction][j] == ' ':
            moves.append((i, j, i + 2*direction, j))

    # Capture moves
    for dj in [-1, 1]:
        if is_valid_position(i + direction, j + dj):
            if board[i + direction][j + dj] != ' ' and \
               (board[i + direction][j + dj].isupper() != (player == 'white')):
                moves.append((i, j, i + direction, j + dj))

    # En passant
    if last_move and abs(last_move[0] - last_move[2]) == 2 and \
       last_move[2] == i and abs(last_move[3] - j) == 1:
        moves.append((i, j, i + direction, last_move[3]))

    return moves

# Get rook moves
def get_rook_moves(board, i, j, player):
    moves = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for di, dj in directions:
        for step in range(1, 8):
            new_i, new_j = i + di * step, j + dj * step
            if not is_valid_position(new_i, new_j):
                break
            if board[new_i][new_j] == ' ':
                moves.append((i, j, new_i, new_j))
            else:
                if (board[new_i][new_j].isupper() and player == 'black') or \
                   (board[new_i][new_j].islower() and player == 'white'):
                    moves.append((i, j, new_i, new_j))
                break
    return moves

# Get knight moves
def get_knight_moves(board, i, j, player):
    moves = []
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1)]
    for di, dj in knight_moves:
        new_i, new_j = i + di, j + dj
        if is_valid_position(new_i, new_j):
            if board[new_i][new_j] == ' ' or \
               (board[new_i][new_j].isupper() and player == 'black') or \
               (board[new_i][new_j].islower() and player == 'white'):
                moves.append((i, j, new_i, new_j))
    return moves

# Get bishop moves
def get_bishop_moves(board, i, j, player):
    moves = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for di, dj in directions:
        for step in range(1, 8):
            new_i, new_j = i + di * step, j + dj * step
            if not is_valid_position(new_i, new_j):
                break
            if board[new_i][new_j] == ' ':
                moves.append((i, j, new_i, new_j))
            else:
                if (board[new_i][new_j].isupper() and player == 'black') or \
                   (board[new_i][new_j].islower() and player == 'white'):
                    moves.append((i, j, new_i, new_j))
                break
    return moves

# Get queen moves (combination of rook and bishop moves)
def get_queen_moves(board, i, j, player):
    return get_rook_moves(board, i, j, player) + get_bishop_moves(board, i, j, player)

# Get king moves (including castling)
def get_king_moves(board, i, j, player):
    moves = []
    king_moves = [(0, 1), (1, 0), (0, -1), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for di, dj in king_moves:
        new_i, new_j = i + di, j + dj
        if is_valid_position(new_i, new_j):
            if board[new_i][new_j] == ' ' or \
               (board[new_i][new_j].isupper() and player == 'black') or \
               (board[new_i][new_j].islower() and player == 'white'):
                moves.append((i, j, new_i, new_j))
    
    # Castling
    if player == 'white' and i == 7 and j == 4:
        if board[7][0] == 'R' and all(board[7][k] == ' ' for k in range(1, 4)):
            moves.append((i, j, i, j-2))  # Queen-side castling
        if board[7][7] == 'R' and all(board[7][k] == ' ' for k in range(5, 7)):
            moves.append((i, j, i, j+2))  # King-side castling
    elif player == 'black' and i == 0 and j == 4:
        if board[0][0] == 'r' and all(board[0][k] == ' ' for k in range(1, 4)):
            moves.append((i, j, i, j-2))  # Queen-side castling
        if board[0][7] == 'r' and all(board[0][k] == ' ' for k in range(5, 7)):
            moves.append((i, j, i, j+2))  # King-side castling
    
    return moves

# Improved evaluation function
def evaluate_board(board):
    piece_values = {'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
                    'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000}
    
    pawn_position_values = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]
    ]

    knight_position_values = [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ]

    bishop_position_values = [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ]

    rook_position_values = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]
    ]

    queen_position_values = [
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [-5,  0,  5,  5,  5,  5,  0, -5],
        [0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]
    ]

    king_position_values = [
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [20, 30, 10,  0,  0, 10, 30, 20]
    ]

    score = 0
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece != ' ':
                score += piece_values.get(piece, 0)
                if piece.lower() == 'p':
                    score += pawn_position_values[i][j] if piece.isupper() else -pawn_position_values[7-i][j]
                elif piece.lower() == 'n':
                    score += knight_position_values[i][j] if piece.isupper() else -knight_position_values[7-i][j]
                elif piece.lower() == 'b':
                    score += bishop_position_values[i][j] if piece.isupper() else -bishop_position_values[7-i][j]
                elif piece.lower() == 'r':
                    score += rook_position_values[i][j] if piece.isupper() else -rook_position_values[7-i][j]
                elif piece.lower() == 'q':
                    score += queen_position_values[i][j] if piece.isupper() else -queen_position_values[7-i][j]
                elif piece.lower() == 'k':
                    score += king_position_values[i][j] if piece.isupper() else -king_position_values[7-i][j]
    
    return score

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player, player, last_move):
    if depth == 0:
        return evaluate_board(board)
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in get_possible_moves(board, player, last_move):
            new_board = [row[:] for row in board]
            make_move(new_board, move)
            eval = minimax(new_board, depth - 1, alpha, beta, False, 'black' if player == 'white' else 'white', move)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_possible_moves(board, player, last_move):
            new_board = [row[:] for row in board]
            make_move(new_board, move)
            eval = minimax(new_board, depth - 1, alpha, beta, True, 'black' if player == 'white' else 'white', move)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# AI move selection
def ai_move(board, player, last_move):
    best_move = None
    best_score = float('-inf') if player == 'white' else float('inf')
    alpha = float('-inf')
    beta = float('inf')
    
    for move in get_possible_moves(board, player, last_move):
        new_board = [row[:] for row in board]
        make_move(new_board, move)
        score = minimax(new_board, 3, alpha, beta, player == 'black', 'black' if player == 'white' else 'white', move)
        
        if player == 'white':
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
        else:
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)
        
        if beta <= alpha:
            break
    
    return best_move

# Make a move on the board (including castling and promotion)
def make_move(board, move):
    i, j, new_i, new_j = move
    piece = board[i][j]
    
    # Castling
    if piece.lower() == 'k' and abs(j - new_j) == 2:
        if new_j > j:  # King-side castling
            board[new_i][new_j-1] = board[new_i][7]
            board[new_i][7] = ' '
        else:  # Queen-side castling
            board[new_i][new_j+1] = board[new_i][0]
            board[new_i][0] = ' '
    
    # En passant capture
    if piece.lower() == 'p' and j != new_j and board[new_i][new_j] == ' ':
        board[i][new_j] = ' '
    
    # Make the move
    board[new_i][new_j] = board[i][j]
    board[i][j] = ' '
    
    # Pawn promotion
    if piece.lower() == 'p' and (new_i == 0 or new_i == 7):
        board[new_i][new_j] = 'Q' if piece.isupper() else 'q'

# Main game loop
def play_game():
    board = init_board()
    current_player = 'white'
    last_move = None
    
    for turn in range(200):  # Increased turn limit
        print(f"\nTurn {turn + 1}")
        print(f"{current_player.capitalize()}'s turn")
        print_board(board)
        
        move = ai_move(board, current_player, last_move)
        if move is None:
            print(f"{current_player.capitalize()} has no valid moves. Game over!")
            return 'black' if current_player == 'white' else 'white'
        
        make_move(board, move)
        print(f"{current_player.capitalize()} moves from {chr(97+move[1])}{8-move[0]} to {chr(97+move[3])}{8-move[2]}")
        
        last_move = move
        current_player = 'black' if current_player == 'white' else 'white'
        
        time.sleep(1)  # Pause for a second between moves
    
    print("Game ended in a draw due to turn limit.")
    return 'draw'

# Play multiple games
def main():
    num_games = 5
    results = {'white': 0, 'black': 0, 'draw': 0}
    
    for game in range(num_games):
        print(f"\n=== Game {game + 1} ===")
        result = play_game()
        results[result] += 1
        print(f"Game {game + 1} result: {result}")
    
    print("\n=== Final Results ===")
    print(f"White wins: {results['white']}")
    print(f"Black wins: {results['black']}")
    print(f"Draws: {results['draw']}")

if __name__ == "__main__":
    main()
