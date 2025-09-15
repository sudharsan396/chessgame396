import pygame
import pygame.font
import sys
import random
import asyncio
import io
import base64
from js import document, window, console

# Web-specific imports and setup
try:
    import pygame.display
    pygame.display.init()
except Exception as e:
    if is_web and console:
        console.log(f"Pygame display init failed (expected in web): {str(e)}")
    pass

# Global variables for web environment
canvas = None
web_surface = None
web_clock = None

# Detect web environment
is_web = True
try:
    import js
    console.log("Running in web environment")
except:
    is_web = False
    console = None

# Initialize Pygame for web
def init_web_game():
    """Initialize the game for web environment"""
    global canvas, web_surface, web_clock

    try:
        # Initialize Pygame (skip display for web)
        if not is_web:
            pygame.init()
        else:
            # Manual initialization for web environment
            pygame.font.init()

        # Set up canvas for web
        canvas = document.getElementById('chess-canvas')
        if canvas:
            # Create surface that matches canvas size
            web_surface = pygame.Surface((canvas.width, canvas.height))
            web_clock = pygame.time.Clock()

            if console:
                console.log(f"Web game initialized with canvas size: {canvas.width}x{canvas.height}")
            return True
        else:
            if console:
                console.log("Canvas not found!")
            return False

    except Exception as e:
        if console:
            console.log(f"Failed to initialize web game: {str(e)}")
        return False

# Screen size for web - will be set dynamically
WIDTH = 680
HEIGHT = 700

# Board setup
SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_WOOD = (139, 69, 19)
LIGHT_WOOD = (222, 184, 135)
BORDER_COLOR = (101, 67, 33)
HIGHLIGHT_COLOR = (255, 215, 0)
TEXT_COLOR = (75, 54, 33)

# Fonts
try:
    coord_font = pygame.font.SysFont('Arial', 16)
    title_font = pygame.font.SysFont('Arial', 24, bold=True)
    font = pygame.font.SysFont('Arial', 24)
    small_font = pygame.font.SysFont('Arial', 18)
except:
    # Fallback fonts for web
    coord_font = pygame.font.Font(None, 16)
    title_font = pygame.font.Font(None, 24)
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 18)

# Chess piece images (will be loaded as base64 or URLs)
images = {}

# Chess board representation
board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

# Game state variables
selected_square = None
game_over = False
winner = None
difficulty = 'medium'  # Default difficulty
game_mode = 'selecting_difficulty'  # 'selecting_difficulty' or 'playing'

# Piece values for AI
piece_values = {
    'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,
    'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0
}

# Game state
selected_square = None
turn = 'w'
game_over = False
winner = None
game_state = 'playing'
difficulty = 'medium'
game_mode = 'selecting_difficulty'

def load_piece_images():
    """Load chess piece images for web environment"""
    global images

    piece_files = {
        'wP': 'wP.png', 'wR': 'wR.png', 'wN': 'wN.png', 'wB': 'wB.png', 'wQ': 'wQ.png', 'wK': 'wK.png',
        'bP': 'bP.png', 'bR': 'bR.png', 'bN': 'bN.png', 'bB': 'bB.png', 'bQ': 'bQ.png', 'bK': 'bK.png'
    }

    for piece, file in piece_files.items():
        try:
            # Try to load from URL first
            img = pygame.image.load(file)
            scaled_size = int(SQUARE_SIZE * 0.8)
            images[piece] = pygame.transform.scale(img, (scaled_size, scaled_size))
            console.log(f"Loaded {file}")
        except Exception as e:
            console.log(f"Could not load {file}: {str(e)}")
            # Create fallback colored rectangle
            fallback_img = pygame.Surface((int(SQUARE_SIZE * 0.8), int(SQUARE_SIZE * 0.8)))
            fallback_img.fill((200, 200, 200))
            images[piece] = fallback_img

def draw_board():
    """Draw the chess board"""
    global web_surface

    if not web_surface:
        return

    # Calculate centered board position
    board_x = (WIDTH - BOARD_SIZE) // 2
    board_y = (HEIGHT - BOARD_SIZE) // 2 + 20

    # Draw outer border
    border_width = max(2, int(SQUARE_SIZE * 0.05))
    pygame.draw.rect(web_surface, BORDER_COLOR,
                     (board_x - border_width//2, board_y - border_width//2,
                      BOARD_SIZE + border_width, BOARD_SIZE + border_width), border_width)

    # Draw chess squares
    for row in range(8):
        for col in range(8):
            x = col * SQUARE_SIZE + board_x
            y = row * SQUARE_SIZE + board_y

            is_light = (row + col) % 2 == 0
            base_color = LIGHT_WOOD if is_light else DARK_WOOD

            # Draw gradient effect
            for i in range(SQUARE_SIZE):
                gradient_factor = i / SQUARE_SIZE
                if is_light:
                    color_top = (min(255, base_color[0] + 20), min(255, base_color[1] + 20), min(255, base_color[2] + 20))
                    color_bottom = base_color
                else:
                    color_top = base_color
                    color_bottom = (max(0, base_color[0] - 30), max(0, base_color[1] - 30), max(0, base_color[2] - 30))

                r = int(color_top[0] + (color_bottom[0] - color_top[0]) * gradient_factor)
                g = int(color_top[1] + (color_bottom[1] - color_top[1]) * gradient_factor)
                b = int(color_top[2] + (color_bottom[2] - color_top[2]) * gradient_factor)
                pygame.draw.line(web_surface, (r, g, b), (x, y + i), (x + SQUARE_SIZE - 1, y + i))

    # Draw coordinate labels
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    numbers = ['8', '7', '6', '5', '4', '3', '2', '1']

    # Bottom letters
    for i, letter in enumerate(letters):
        text = coord_font.render(letter, True, TEXT_COLOR)
        x = board_x + i * SQUARE_SIZE + SQUARE_SIZE//2 - text.get_width()//2
        y = board_y + BOARD_SIZE + border_width//2
        web_surface.blit(text, (x, y))

    # Side numbers
    for i, number in enumerate(numbers):
        text = coord_font.render(number, True, TEXT_COLOR)
        x = board_x - text.get_width() - border_width//2
        y = board_y + i * SQUARE_SIZE + SQUARE_SIZE//2 - text.get_height()//2
        web_surface.blit(text, (x, y))

    # Draw title
    title = title_font.render("CHESS MASTER", True, HIGHLIGHT_COLOR)
    title_x = WIDTH//2 - title.get_width()//2
    title_y = 10
    web_surface.blit(title, (title_x, title_y))

    # Draw difficulty indicator
    difficulty_colors = {'easy': (100, 200, 100), 'medium': (255, 165, 0), 'hard': (200, 50, 50)}
    diff_color = difficulty_colors.get(difficulty, (255, 255, 255))
    diff_text = small_font.render(f"Difficulty: {difficulty.upper()}", True, diff_color)
    diff_x = WIDTH - diff_text.get_width() - 10
    diff_y = 10
    web_surface.blit(diff_text, (diff_x, diff_y))

def draw_pieces():
    """Draw chess pieces on the board"""
    global web_surface

    if not web_surface:
        return

    board_x = (WIDTH - BOARD_SIZE) // 2
    board_y = (HEIGHT - BOARD_SIZE) // 2 + 20

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--' and piece in images:
                img = images[piece]
                x = col * SQUARE_SIZE + board_x + (SQUARE_SIZE - img.get_width()) // 2
                y = row * SQUARE_SIZE + board_y + (SQUARE_SIZE - img.get_height()) // 2
                web_surface.blit(img, (x, y))

def draw_check_indicator():
    """Draw red border around king if in check"""
    global web_surface

    if not web_surface:
        return

    board_x = (WIDTH - BOARD_SIZE) // 2
    board_y = (HEIGHT - BOARD_SIZE) // 2 + 20

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--' and piece[1] == 'K':
                king_color = piece[0]
                if is_king_in_check(board, king_color):
                    x = col * SQUARE_SIZE + board_x
                    y = row * SQUARE_SIZE + board_y
                    pygame.draw.rect(web_surface, (255, 0, 0), (x, y, SQUARE_SIZE, SQUARE_SIZE), 4)

def draw_touch_feedback():
    """Draw visual feedback for selected piece"""
    global web_surface

    if not web_surface or selected_square is None:
        return

    board_x = (WIDTH - BOARD_SIZE) // 2
    board_y = (HEIGHT - BOARD_SIZE) // 2 + 20

    row, col = selected_square
    x = col * SQUARE_SIZE + board_x
    y = row * SQUARE_SIZE + board_y

    # Draw selection highlight
    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
    highlight_surface.set_alpha(100)
    highlight_surface.fill((255, 255, 0))
    web_surface.blit(highlight_surface, (x, y))

    # Draw border
    pygame.draw.rect(web_surface, (255, 255, 0), (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)

def get_valid_moves_for_piece(row, col):
    """Get all valid moves for a piece"""
    valid_moves = []
    valid_captures = []

    if board[row][col] == '--':
        return valid_moves, valid_captures

    for end_row in range(8):
        for end_col in range(8):
            if is_valid_move(row, col, end_row, end_col):
                if board[end_row][end_col] == '--':
                    valid_moves.append((end_row, end_col))
                else:
                    valid_captures.append((end_row, end_col))

    return valid_moves, valid_captures

def draw_move_paths():
    """Draw visual indicators for valid moves"""
    global web_surface

    if not web_surface or selected_square is None:
        return

    board_x = (WIDTH - BOARD_SIZE) // 2
    board_y = (HEIGHT - BOARD_SIZE) // 2 + 20

    valid_moves, valid_captures = get_valid_moves_for_piece(selected_square[0], selected_square[1])

    # Draw valid moves (green circles)
    for move_row, move_col in valid_moves:
        x = move_col * SQUARE_SIZE + board_x + SQUARE_SIZE // 2
        y = move_row * SQUARE_SIZE + board_y + SQUARE_SIZE // 2

        radius = max(8, SQUARE_SIZE // 6)
        pygame.draw.circle(web_surface, (0, 150, 0), (x, y), radius + 3, 2)
        pygame.draw.circle(web_surface, (0, 255, 0), (x, y), radius)

    # Draw valid captures (red circles with X)
    for capture_row, capture_col in valid_captures:
        x = capture_col * SQUARE_SIZE + board_x + SQUARE_SIZE // 2
        y = capture_row * SQUARE_SIZE + board_y + SQUARE_SIZE // 2

        radius = max(10, SQUARE_SIZE // 5)
        pygame.draw.circle(web_surface, (150, 0, 0), (x, y), radius + 4, 3)
        pygame.draw.circle(web_surface, (255, 0, 0), (x, y), radius)

        # Draw X mark
        cross_size = max(4, SQUARE_SIZE // 12)
        pygame.draw.line(web_surface, (255, 255, 255), (x - cross_size, y - cross_size), (x + cross_size, y + cross_size), 2)
        pygame.draw.line(web_surface, (255, 255, 255), (x + cross_size, y - cross_size), (x - cross_size, y + cross_size), 2)

def get_square_from_pos(pos):
    """Convert screen position to board coordinates"""
    board_x = (WIDTH - BOARD_SIZE) // 2
    board_y = (HEIGHT - BOARD_SIZE) // 2 + 20

    x, y = pos
    x -= board_x
    y -= board_y

    if x < 0 or y < 0 or x >= BOARD_SIZE or y >= BOARD_SIZE:
        return -1, -1

    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col

# Include all the game logic functions from the original chess.py
# (is_valid_move, make_move, get_random_move, evaluate_board, minimax, etc.)

def is_valid_move(start_row, start_col, end_row, end_col):
    """Validate chess moves"""
    if start_row == end_row and start_col == end_col:
        return False

    piece = board[start_row][start_col]
    if piece == '--':
        return False

    target_piece = board[end_row][end_col]
    if target_piece != '--' and target_piece[0] == piece[0]:
        return False

    piece_type = piece[1]
    color = piece[0]

    move_valid = False

    # Pawn movement
    if piece_type == 'P':
        direction = -1 if color == 'w' else 1
        if start_col == end_col:
            if target_piece == '--':
                if end_row == start_row + direction:
                    move_valid = True
                elif end_row == start_row + 2 * direction and start_row == (6 if color == 'w' else 1):
                    move_valid = board[start_row + direction][start_col] == '--'
        elif abs(start_col - end_col) == 1 and end_row == start_row + direction:
            move_valid = target_piece != '--' and target_piece[0] != color

    # Rook movement
    elif piece_type == 'R':
        if start_row == end_row:
            step = 1 if end_col > start_col else -1
            path_clear = True
            for col in range(start_col + step, end_col, step):
                if board[start_row][col] != '--':
                    path_clear = False
                    break
            move_valid = path_clear
        elif start_col == end_col:
            step = 1 if end_row > start_row else -1
            path_clear = True
            for row in range(start_row + step, end_row, step):
                if board[row][start_col] != '--':
                    path_clear = False
                    break
            move_valid = path_clear

    # Bishop movement
    elif piece_type == 'B':
        if abs(start_row - end_row) == abs(start_col - end_col):
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            path_clear = True
            row, col = start_row + row_step, start_col + col_step
            while row != end_row:
                if board[row][col] != '--':
                    path_clear = False
                    break
                row += row_step
                col += col_step
            move_valid = path_clear

    # Queen movement
    elif piece_type == 'Q':
        if start_row == end_row or start_col == end_col:
            if start_row == end_row:
                step = 1 if end_col > start_col else -1
                path_clear = True
                for col in range(start_col + step, end_col, step):
                    if board[start_row][col] != '--':
                        path_clear = False
                        break
                move_valid = path_clear
            else:
                step = 1 if end_row > start_row else -1
                path_clear = True
                for row in range(start_row + step, end_row, step):
                    if board[row][start_col] != '--':
                        path_clear = False
                        break
                move_valid = path_clear
        elif abs(start_row - end_row) == abs(start_col - end_col):
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            path_clear = True
            row, col = start_row + row_step, start_col + col_step
            while row != end_row:
                if board[row][col] != '--':
                    path_clear = False
                    break
                row += row_step
                col += col_step
            move_valid = path_clear

    # Knight movement
    elif piece_type == 'N':
        move_valid = (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
                     (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2)

    # King movement
    elif piece_type == 'K':
        move_valid = abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1

    if not move_valid:
        return False

    # Check if move would leave king in check
    temp_board = [row[:] for row in board]
    temp_board[end_row][end_col] = temp_board[start_row][start_col]
    temp_board[start_row][start_col] = '--'

    if is_king_in_check(temp_board, color):
        return False

    return True

def make_move(start_row, start_col, end_row, end_col):
    """Execute a move"""
    global turn
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = '--'
    turn = 'b' if turn == 'w' else 'w'
    check_game_state()

def get_random_move():
    """Get random move for easy difficulty"""
    moves = []
    for row in range(8):
        for col in range(8):
            if board[row][col][0] == turn:
                for end_row in range(8):
                    for end_col in range(8):
                        if is_valid_move(row, col, end_row, end_col):
                            moves.append((row, col, end_row, end_col))
    if moves:
        return random.choice(moves)
    return None

def evaluate_board(board):
    """Simple board evaluation for AI"""
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--':
                value = piece_values.get(piece[1], 0)
                center_bonus = 0
                if 2 <= row <= 5 and 2 <= col <= 5:
                    center_bonus = 0.1 * value
                multiplier = 1 if piece[0] == 'b' else -1
                score += multiplier * (value + center_bonus)
    return score

def minimax(board, depth, alpha, beta, maximizing_player):
    """Minimax algorithm with alpha-beta pruning"""
    if depth == 0 or game_over:
        return evaluate_board(board), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        moves = get_all_moves(board, 'b')
        for move in moves:
            temp_board = [row[:] for row in board]
            temp_board[move[2]][move[3]] = temp_board[move[0]][move[1]]
            temp_board[move[0]][move[1]] = '--'
            eval_score, _ = minimax(temp_board, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        moves = get_all_moves(board, 'w')
        for move in moves:
            temp_board = [row[:] for row in board]
            temp_board[move[2]][move[3]] = temp_board[move[0]][move[1]]
            temp_board[move[0]][move[1]] = '--'
            eval_score, _ = minimax(temp_board, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def get_all_moves(board, color):
    """Get all valid moves for a color"""
    moves = []
    for row in range(8):
        for col in range(8):
            if board[row][col][0] == color:
                for end_row in range(8):
                    for end_col in range(8):
                        if is_valid_move(row, col, end_row, end_col):
                            moves.append((row, col, end_row, end_col))
    return moves

def get_computer_move(difficulty):
    """Get computer move based on difficulty"""
    if difficulty == 'easy':
        return get_random_move()
    elif difficulty == 'medium':
        moves = get_all_moves(board, turn)
        if not moves:
            return None

        best_move = None
        best_score = float('-inf')

        for move in moves:
            temp_board = [row[:] for row in board]
            temp_board[move[2]][move[3]] = temp_board[move[0]][move[1]]
            temp_board[move[0]][move[1]] = '--'
            score = evaluate_board(temp_board)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move if best_move else random.choice(moves)
    elif difficulty == 'hard':
        _, best_move = minimax(board, 2, float('-inf'), float('inf'), True)
        return best_move
    else:
        return get_random_move()

def is_king_in_check(board, king_color):
    """Check if king is in check"""
    king_pos = None
    for row in range(8):
        for col in range(8):
            if board[row][col] == king_color + 'K':
                king_pos = (row, col)
                break
        if king_pos:
            break

    if not king_pos:
        return False

    opponent_color = 'b' if king_color == 'w' else 'w'
    for row in range(8):
        for col in range(8):
            if board[row][col][0] == opponent_color:
                if can_piece_attack_square(board, row, col, king_pos[0], king_pos[1]):
                    return True
    return False

def can_piece_attack_square(board, start_row, start_col, end_row, end_col):
    """Check if piece can attack square"""
    if start_row == end_row and start_col == end_col:
        return False

    piece = board[start_row][start_col]
    if piece == '--':
        return False

    target_piece = board[end_row][end_col]
    if target_piece != '--' and target_piece[0] == piece[0]:
        return False

    piece_type = piece[1]

    # Pawn attack
    if piece_type == 'P':
        color = piece[0]
        direction = -1 if color == 'w' else 1
        if abs(start_col - end_col) == 1 and end_row == start_row + direction:
            return True

    # Rook movement
    elif piece_type == 'R':
        if start_row == end_row:
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if board[start_row][col] != '--':
                    return False
            return True
        elif start_col == end_col:
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if board[row][start_col] != '--':
                    return False
            return True

    # Bishop movement
    elif piece_type == 'B':
        if abs(start_row - end_row) == abs(start_col - end_col):
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            row, col = start_row + row_step, start_col + col_step
            while row != end_row:
                if board[row][col] != '--':
                    return False
                row += row_step
                col += col_step
            return True

    # Queen movement
    elif piece_type == 'Q':
        if start_row == end_row or start_col == end_col:
            if start_row == end_row:
                step = 1 if end_col > start_col else -1
                for col in range(start_col + step, end_col, step):
                    if board[start_row][col] != '--':
                        return False
            else:
                step = 1 if end_row > start_row else -1
                for row in range(start_row + step, end_row, step):
                    if board[row][start_col] != '--':
                        return False
            return True
        elif abs(start_row - end_row) == abs(start_col - end_col):
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            row, col = start_row + row_step, start_col + col_step
            while row != end_row:
                if board[row][col] != '--':
                    return False
                row += row_step
                col += col_step
            return True

    # Knight movement
    elif piece_type == 'N':
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
           (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return True

    # King movement
    elif piece_type == 'K':
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return True

    return False

def has_legal_moves(board, color):
    """Check if color has legal moves"""
    for row in range(8):
        for col in range(8):
            if board[row][col][0] == color:
                for end_row in range(8):
                    for end_col in range(8):
                        if is_valid_move(row, col, end_row, end_col):
                            return True
    return False

def check_game_state():
    """Check game state for win/loss/draw"""
    global game_state, winner, game_over

    white_in_check = is_king_in_check(board, 'w')
    black_in_check = is_king_in_check(board, 'b')
    white_has_moves = has_legal_moves(board, 'w')
    black_has_moves = has_legal_moves(board, 'b')

    console.log(f"Debug: White in check: {white_in_check}, White has moves: {white_has_moves}")
    console.log(f"Debug: Black in check: {black_in_check}, Black has moves: {black_has_moves}")
    console.log(f"Debug: Current turn: {turn}, Game over: {game_over}")

    if turn == 'w':
        if not white_has_moves:
            if white_in_check:
                game_state = 'black_wins'
                winner = 'Black'
                game_over = True
                console.log("Debug: Black wins by checkmate!")
            else:
                game_state = 'draw'
                winner = None
                game_over = True
                console.log("Debug: Stalemate - Draw!")
    else:
        if not black_has_moves:
            if black_in_check:
                game_state = 'white_wins'
                winner = 'White'
                game_over = True
                console.log("Debug: White wins by checkmate!")
            else:
                game_state = 'draw'
                winner = None
                game_over = True
                console.log("Debug: Stalemate - Draw!")

def reset_game():
    """Reset game to initial state"""
    global board, selected_square, turn, game_over, winner, game_state, game_mode

    board = [
        ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
        ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
        ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
    ]

    selected_square = None
    turn = 'w'
    game_over = False
    winner = None
    game_state = 'playing'
    game_mode = 'selecting_difficulty'

def draw_win_screen():
    """Draw win/lose/draw screen"""
    global web_surface

    if not web_surface:
        return

    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))
    web_surface.blit(overlay, (0, 0))

    # Message based on game state
    if game_state == 'white_wins':
        message = "🎉 CONGRATULATIONS! 🎉"
        sub_message = "You Won the Game!"
        color = (0, 255, 0)
    elif game_state == 'black_wins':
        message = "😔 COMPUTER WINS! 😔"
        sub_message = "Better luck next time!"
        color = (255, 0, 0)
    else:
        message = "🤝 IT'S A DRAW! 🤝"
        sub_message = "Well played!"
        color = (255, 255, 0)

    # Draw main message
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
    web_surface.blit(text, text_rect)

    # Draw sub message
    sub_text = small_font.render(sub_message, True, (255, 255, 255))
    sub_rect = sub_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
    web_surface.blit(sub_text, sub_rect)

    # Draw restart instruction
    restart_text = small_font.render("Click anywhere to play again", True, (220, 220, 220))
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
    web_surface.blit(restart_text, restart_rect)

# Web-specific functions
def set_difficulty(new_difficulty):
    """Set game difficulty"""
    global difficulty
    difficulty = new_difficulty
    console.log(f"Difficulty set to: {difficulty}")

def new_game():
    """Start new game"""
    global game_mode
    reset_game()
    game_mode = 'playing'
    console.log("New game started")

def handle_resize():
    """Handle window resize"""
    global WIDTH, HEIGHT, BOARD_SIZE, SQUARE_SIZE, web_surface

    if canvas:
        WIDTH = canvas.width
        HEIGHT = canvas.height
        BOARD_SIZE = min(WIDTH, HEIGHT) - 40
        SQUARE_SIZE = BOARD_SIZE // 8

        # Recreate surface with new size
        web_surface = pygame.Surface((WIDTH, HEIGHT))

        console.log(f"Resized to: {WIDTH}x{HEIGHT}")

def handle_mouse_click(x, y):
    """Handle mouse click event from JavaScript"""
    global selected_square, game_over

    console.log(f"Mouse click at: ({x}, {y})")

    if game_over:
        reset_game()
        return

    if game_mode == 'selecting_difficulty':
        return

    row, col = get_square_from_pos((x, y))

    if row >= 0 and col >= 0:
        if selected_square is None:
            # Select piece
            if board[row][col][0] == 'w':  # White pieces (player)
                selected_square = (row, col)
                console.log(f"Selected piece at ({row}, {col})")
        else:
            # Try to move selected piece
            start_row, start_col = selected_square
            if is_valid_move(start_row, start_col, row, col):
                make_move(start_row, start_col, row, col)
                selected_square = None
                console.log(f"Moved piece from ({start_row}, {start_col}) to ({row}, {col})")

                # Computer's turn
                if not game_over:
                    move = get_computer_move(difficulty)
                    if move:
                        make_move(*move)
                        console.log(f"Computer moved from ({move[0]}, {move[1]}) to ({move[2]}, {move[3]})")
            else:
                selected_square = None
                console.log(f"Invalid move from ({start_row}, {start_col}) to ({row}, {col})")

def handle_touch_event(x, y):
    """Handle touch event from JavaScript"""
    handle_mouse_click(x, y)

def update_display():
    """Update the display - called from JavaScript"""
    global web_surface, canvas

    if not web_surface or not canvas:
        return

    # Clear surface
    web_surface.fill((0, 0, 0))

    # Draw game elements
    draw_board()
    draw_pieces()
    draw_check_indicator()
    draw_touch_feedback()
    draw_move_paths()

    if game_over:
        draw_win_screen()

    # Copy to canvas
    try:
        # Get canvas context
        ctx = canvas.getContext('2d')

        # Convert pygame surface to canvas
        # This is a simplified approach - in practice, you'd need more complex conversion
        # For now, we'll just update the status
        pass

    except Exception as e:
        console.log(f"Display update error: {str(e)}")

# Web-specific functions for JavaScript integration
def set_difficulty(new_difficulty):
    """Set game difficulty from JavaScript"""
    global difficulty
    difficulty = new_difficulty
    if console:
        console.log(f"Difficulty set to: {difficulty}")

def new_game():
    """Start new game from JavaScript"""
    global game_mode, selected_square
    reset_game()
    game_mode = 'playing'
    selected_square = None
    if console:
        console.log("New game started")

def handle_resize():
    """Handle window resize from JavaScript"""
    global WIDTH, HEIGHT, BOARD_SIZE, SQUARE_SIZE, web_surface

    if canvas:
        WIDTH = canvas.width
        HEIGHT = canvas.height
        BOARD_SIZE = min(WIDTH, HEIGHT) - 40
        SQUARE_SIZE = BOARD_SIZE // 8

        # Recreate surface with new size
        web_surface = pygame.Surface((WIDTH, HEIGHT))

        if console:
            console.log(f"Resized to: {WIDTH}x{HEIGHT}")

def draw_win_screen():
    """Draw the winning screen"""
    global web_surface

    if not web_surface:
        return

    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    web_surface.blit(overlay, (0, 0))

    # Win message
    font = pygame.font.Font(None, 72)
    if winner == 'white':
        text = font.render("You Win!", True, (255, 255, 255))
    elif winner == 'black':
        text = font.render("Computer Wins!", True, (255, 255, 255))
    else:
        text = font.render("Game Over!", True, (255, 255, 255))

    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    web_surface.blit(text, text_rect)

    # Subtitle
    font_small = pygame.font.Font(None, 36)
    subtitle = font_small.render("Press SPACE for new game", True, (200, 200, 200))
    subtitle_rect = subtitle.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
    web_surface.blit(subtitle, subtitle_rect)

# Initialize the game when module loads
if is_web:
    console.log("Chess Web Module Loaded")
    load_piece_images()