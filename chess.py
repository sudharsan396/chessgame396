import pygame
import sys
import random

# Detect if running on Pydroid3
is_pydroid3 = False
try:
    import os
    if os.name == 'posix':
        # Check for Pydroid3-specific indicators
        if hasattr(os, 'environ') and ('ANDROID_DATA' in os.environ or 'PYDROID3' in str(os.environ)):
            is_pydroid3 = True
        # Also check if pygame version indicates mobile
        if hasattr(pygame, 'version') and 'SDL' in str(pygame.version.ver):
            is_pydroid3 = True
except:
    pass

print(f"Pydroid3: Running on Pydroid3: {is_pydroid3}")

# Initialize Pygame - Pydroid3 compatible
try:
    pygame.init()
    print("Pydroid3: Pygame initialized successfully")
except Exception as e:
    print(f"Pydroid3: Pygame init error: {e}")
    raise

# Get screen size for mobile compatibility - Pydroid3 safe
try:
    info = pygame.display.Info()
    screen_width = int(info.current_w) if hasattr(info, 'current_w') and info.current_w and info.current_w > 0 else 640
    screen_height = int(info.current_h) if hasattr(info, 'current_h') and info.current_h and info.current_h > 0 else 640
except Exception as e:
    print(f"Pydroid3: pygame.display.Info() failed: {e}")
    # Pydroid3 safe fallback
    screen_width = 640
    screen_height = 640

print(f"Pydroid3: Detected screen size: {screen_width}x{screen_height}")

# For mobile devices, try to get the actual display size
try:
    import os
    if os.name == 'posix':  # Likely Android/iOS
        # Try to get display metrics for mobile
        try:
            # For Pydroid3/Android, try to get screen size from environment
            screen_width = int(os.environ.get('DISPLAY_WIDTH', screen_width))
            screen_height = int(os.environ.get('DISPLAY_HEIGHT', screen_height))
        except:
            pass
except:
    pass

# Ensure minimum screen size for mobile - increased for better visibility
screen_width = max(screen_width, 600)  # Increased from 400
screen_height = max(screen_height, 600)  # Increased from 400

# For mobile, use full screen mode to maximize board size
try:
    # Try fullscreen mode first for mobile
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
    print(f"Fullscreen mode: {screen_width}x{screen_height}")
except:
    # Fallback to windowed mode
    pass

# Adjust board size to maximize screen usage
# Use more aggressive sizing for mobile
available_width = screen_width - 40  # Less border space
available_height = screen_height - 80  # Less space for title

# Calculate optimal square size
max_square_from_width = available_width // 8
max_square_from_height = available_height // 8
SQUARE_SIZE = min(max_square_from_width, max_square_from_height)

# Ensure minimum and maximum sizes
SQUARE_SIZE = max(40, min(SQUARE_SIZE, 80))  # Min 40, Max 80 for mobile

# Ensure SQUARE_SIZE is an integer
SQUARE_SIZE = int(SQUARE_SIZE)

# Calculate final dimensions
WIDTH = SQUARE_SIZE * 8 + 40  # Minimal border space
HEIGHT = SQUARE_SIZE * 8 + 60  # Space for title

print(f"Mobile optimized: Screen {screen_width}x{screen_height}, Board {WIDTH}x{HEIGHT}, Square {SQUARE_SIZE}")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Enhanced colors for beautiful board
DARK_WOOD = (139, 69, 19)      # Saddle brown
LIGHT_WOOD = (222, 184, 135)   # Burlywood
BORDER_COLOR = (101, 67, 33)   # Dark brown border
HIGHLIGHT_COLOR = (255, 215, 0)  # Gold for highlights
SHADOW_COLOR = (0, 0, 0, 50)   # Semi-transparent black
TEXT_COLOR = (75, 54, 33)      # Dark brown for text

# Fonts for coordinates and title - optimized for mobile
coord_font = pygame.font.SysFont('Arial', max(16, int(SQUARE_SIZE * 0.3)))  # Larger for mobile
title_font = pygame.font.SysFont('Arial', max(20, int(SQUARE_SIZE * 0.4)), bold=True)  # Larger for mobile
font = pygame.font.SysFont('Arial', max(24, int(SQUARE_SIZE * 0.5)))  # Larger for mobile
small_font = pygame.font.SysFont('Arial', max(18, int(SQUARE_SIZE * 0.35)))  # Larger for mobile

# Piece images - Pydroid3 compatible
images = {}
piece_files = {
    'wP': 'wP.png', 'wR': 'wR.png', 'wN': 'wN.png', 'wB': 'wB.png', 'wQ': 'wQ.png', 'wK': 'wK.png',
    'bP': 'bP.png', 'bR': 'bR.png', 'bN': 'bN.png', 'bB': 'bB.png', 'bQ': 'bQ.png', 'bK': 'bK.png'
}

for piece, file in piece_files.items():
    try:
        img = pygame.image.load(file)
        # Scale image to fit square (leave some margin)
        scaled_size = int(SQUARE_SIZE * 0.8)
        images[piece] = pygame.transform.scale(img, (scaled_size, scaled_size))
        print(f"Pydroid3: Loaded {file}")
    except Exception as e:
        print(f"Pydroid3: Could not load {file}: {e}")
        # Create a simple colored rectangle as fallback
        fallback_img = pygame.Surface((int(SQUARE_SIZE * 0.8), int(SQUARE_SIZE * 0.8)))
        fallback_img.fill((200, 200, 200))  # Light gray
        images[piece] = fallback_img

# Board representation
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

# Piece values for AI
piece_values = {
    'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,
    'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0
}

# Game state
selected_square = None
turn = 'w'  # w for white, b for black
game_over = False
winner = None
game_state = 'playing'  # 'playing', 'white_wins', 'black_wins', 'draw'

# Fonts - mobile optimized
font = pygame.font.SysFont('Arial', max(24, int(SQUARE_SIZE * 0.5)))
small_font = pygame.font.SysFont('Arial', max(18, int(SQUARE_SIZE * 0.35)))

# Screen initialization with mobile optimizations - Pydroid3 compatible
try:
    # For Pydroid3, use windowed mode instead of fullscreen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess Master - Mobile')
    print(f"Pydroid3 windowed mode initialized: {WIDTH}x{HEIGHT}")
except Exception as e:
    print(f"Pydroid3 initialization failed: {e}")
    # Emergency fallback for Pydroid3
    try:
        WIDTH = 640
        HEIGHT = 640
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        print(f"Pydroid3 emergency fallback: {WIDTH}x{HEIGHT}")
    except Exception as e2:
        print(f"Pydroid3 emergency fallback failed: {e2}")
        # Last resort - minimal mode
        screen = pygame.display.set_mode((400, 400))
        WIDTH, HEIGHT = 400, 400
        pygame.display.set_caption('Chess')
        print("Pydroid3 minimal mode: 400x400")

def draw_board():
    # Calculate centered board position
    board_size = SQUARE_SIZE * 8
    board_x = (WIDTH - board_size) // 2  # Center horizontally
    board_y = (HEIGHT - board_size) // 2 + 20  # Center vertically with some top space for title

    # Draw outer border with minimal space for mobile
    border_width = max(2, int(SQUARE_SIZE * 0.05))  # Smaller border for mobile

    # Shadow for depth
    pygame.draw.rect(screen, (0, 0, 0, 100),
                     (board_x - border_width//2, board_y - border_width//2,
                      board_size + border_width, board_size + border_width))

    # Main border
    pygame.draw.rect(screen, BORDER_COLOR,
                     (board_x - border_width//2, board_y - border_width//2,
                      board_size + border_width, board_size + border_width), border_width)

    # Inner highlight border
    pygame.draw.rect(screen, HIGHLIGHT_COLOR,
                     (board_x - border_width//4, board_y - border_width//4,
                      board_size + border_width//2, board_size + border_width//2), 1)

    # Draw chess squares with enhanced colors and effects
    for row in range(8):
        for col in range(8):
            x = col * SQUARE_SIZE + board_x
            y = row * SQUARE_SIZE + board_y

            # Base color
            is_light = (row + col) % 2 == 0
            base_color = LIGHT_WOOD if is_light else DARK_WOOD

            # Create gradient effect
            if is_light:
                # Light square gradient (lighter at top-left)
                color_top = (
                    min(255, base_color[0] + 20),
                    min(255, base_color[1] + 20),
                    min(255, base_color[2] + 20)
                )
                color_bottom = base_color
            else:
                # Dark square gradient (darker at bottom-right)
                color_top = base_color
                color_bottom = (
                    max(0, base_color[0] - 30),
                    max(0, base_color[1] - 30),
                    max(0, base_color[2] - 30)
                )

            # Draw gradient square
            for i in range(SQUARE_SIZE):
                gradient_factor = i / SQUARE_SIZE
                r = int(color_top[0] + (color_bottom[0] - color_top[0]) * gradient_factor)
                g = int(color_top[1] + (color_bottom[1] - color_top[1]) * gradient_factor)
                b = int(color_top[2] + (color_bottom[2] - color_top[2]) * gradient_factor)
                pygame.draw.line(screen, (r, g, b), (x, y + i), (x + SQUARE_SIZE - 1, y + i))

            # Add wood grain effect (subtle lines)
            if not is_light:
                for i in range(0, SQUARE_SIZE, 6):  # Less frequent for mobile
                    alpha = 30 + (i % 20)
                    grain_color = (
                        min(255, base_color[0] + alpha),
                        min(255, base_color[1] + alpha//2),
                        min(255, base_color[2] + alpha//3)
                    )
                    pygame.draw.line(screen, grain_color, (x, y + i), (x + SQUARE_SIZE, y + i), 1)

    # Draw coordinate labels with adjusted positioning
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    numbers = ['8', '7', '6', '5', '4', '3', '2', '1']

    # Bottom letters (a-h)
    for i, letter in enumerate(letters):
        text = coord_font.render(letter, True, TEXT_COLOR)
        x = board_x + i * SQUARE_SIZE + SQUARE_SIZE//2 - text.get_width()//2
        y = board_y + board_size + border_width//2
        screen.blit(text, (x, y))

    # Side numbers (8-1)
    for i, number in enumerate(numbers):
        text = coord_font.render(number, True, TEXT_COLOR)
        x = board_x - text.get_width() - border_width//2
        y = board_y + i * SQUARE_SIZE + SQUARE_SIZE//2 - text.get_height()//2
        screen.blit(text, (x, y))

    # Draw title with better mobile positioning
    title = title_font.render("CHESS MASTER", True, HIGHLIGHT_COLOR)
    title_x = WIDTH//2 - title.get_width()//2
    title_y = 10  # Higher up for mobile
    screen.blit(title, (title_x, title_y))

def draw_pieces():
    # Calculate centered board position (same as in draw_board)
    board_size = SQUARE_SIZE * 8
    board_x = (WIDTH - board_size) // 2  # Center horizontally
    board_y = (HEIGHT - board_size) // 2 + 20  # Center vertically with some top space for title

    # Check if we have any images loaded
    has_images = any(images.get(piece) is not None for row in board for piece in row if piece != '--')

    if has_images:
        # Use image-based pieces
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '--' and piece in images and images[piece] is not None:
                    img = images[piece]
                    # Position pieces within the centered board
                    x = col * SQUARE_SIZE + board_x + (SQUARE_SIZE - img.get_width()) // 2
                    y = row * SQUARE_SIZE + board_y + (SQUARE_SIZE - img.get_height()) // 2
                    screen.blit(img, (x, y))
    else:
        # Use text-based fallback
        print("Pydroid3: Using text-based piece display")
        draw_pieces_text_fallback()

def draw_pieces_text_fallback():
    """Text-based fallback for pieces when images fail to load"""
    # Calculate centered board position (same as in draw_board)
    board_size = SQUARE_SIZE * 8
    board_x = (WIDTH - board_size) // 2  # Center horizontally
    board_y = (HEIGHT - board_size) // 2 + 20  # Center vertically with some top space for title

    piece_symbols = {
        'wP': '♙', 'wR': '♖', 'wN': '♘', 'wB': '♗', 'wQ': '♕', 'wK': '♔',
        'bP': '♟', 'bR': '♜', 'bN': '♞', 'bB': '♝', 'bQ': '♛', 'bK': '♚'
    }

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--':
                # Position for text piece
                x = col * SQUARE_SIZE + board_x + SQUARE_SIZE//2
                y = row * SQUARE_SIZE + board_y + SQUARE_SIZE//2

                # Draw text symbol
                symbol = piece_symbols.get(piece, '?')
                text = font.render(symbol, True, (0, 0, 0) if piece[0] == 'w' else (255, 255, 255))
                text_rect = text.get_rect(center=(x, y))
                screen.blit(text, text_rect)

def draw_check_indicator():
    """Draw a red border around the king if it's in check"""
    # Calculate centered board position (same as in draw_board)
    board_size = SQUARE_SIZE * 8
    board_x = (WIDTH - board_size) // 2  # Center horizontally
    board_y = (HEIGHT - board_size) // 2 + 20  # Center vertically with some top space for title

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--' and piece[1] == 'K':  # Found a king
                king_color = piece[0]
                if is_king_in_check(board, king_color):
                    # Draw red border around the king with centered positioning
                    x = col * SQUARE_SIZE + board_x
                    y = row * SQUARE_SIZE + board_y

                    # Draw red rectangle around the square
                    red_border = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    red_border.set_alpha(150)  # Semi-transparent
                    red_border.fill((255, 0, 0))  # Red color

                    # Create a border effect by drawing a thinner inner rectangle
                    inner_size = SQUARE_SIZE - 8
                    inner_x = (SQUARE_SIZE - inner_size) // 2
                    inner_y = (SQUARE_SIZE - inner_size) // 2

                    # Draw the red border
                    pygame.draw.rect(screen, (255, 0, 0), (x, y, SQUARE_SIZE, SQUARE_SIZE), 4)

                    # Add a pulsing effect with alternating border thickness
                    import time
                    if int(time.time() * 2) % 2 == 0:
                        pygame.draw.rect(screen, (255, 100, 100), (x+2, y+2, SQUARE_SIZE-4, SQUARE_SIZE-4), 2)

def draw_touch_feedback():
    """Draw visual feedback for touch interactions"""
    if selected_square is not None:
        # Calculate centered board position
        board_size = SQUARE_SIZE * 8
        board_x = (WIDTH - board_size) // 2
        board_y = (HEIGHT - board_size) // 2 + 20

        row, col = selected_square
        x = col * SQUARE_SIZE + board_x
        y = row * SQUARE_SIZE + board_y

        # Draw selection highlight
        highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        highlight_surface.set_alpha(100)
        highlight_surface.fill((255, 255, 0))  # Yellow highlight
        screen.blit(highlight_surface, (x, y))

        # Draw border around selected piece
        pygame.draw.rect(screen, (255, 255, 0), (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)

def get_square_from_pos(pos):
    # Calculate centered board position (same as in draw_board)
    board_size = SQUARE_SIZE * 8
    board_x = (WIDTH - board_size) // 2  # Center horizontally
    board_y = (HEIGHT - board_size) // 2 + 20  # Center vertically with some top space for title

    x, y = pos
    # Adjust for centered board offset
    x -= board_x
    y -= board_y
    if x < 0 or y < 0 or x >= board_size or y >= board_size:
        return -1, -1  # Invalid position
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col

def is_valid_move(start_row, start_col, end_row, end_col):
    if start_row == end_row and start_col == end_col:
        return False

    piece = board[start_row][start_col]
    if piece == '--':
        return False

    target_piece = board[end_row][end_col]
    if target_piece != '--' and target_piece[0] == piece[0]:  # Same color
        return False

    piece_type = piece[1]
    color = piece[0]

    # Basic movement validation
    move_valid = False

    # Pawn movement
    if piece_type == 'P':
        direction = -1 if color == 'w' else 1
        if start_col == end_col:  # Forward move
            if target_piece == '--':  # Must be empty
                if end_row == start_row + direction:
                    move_valid = True
                elif end_row == start_row + 2 * direction and start_row == (6 if color == 'w' else 1):
                    # Check if path is clear for double move
                    move_valid = board[start_row + direction][start_col] == '--'
        elif abs(start_col - end_col) == 1 and end_row == start_row + direction:
            # Diagonal capture
            move_valid = target_piece != '--' and target_piece[0] != color

    # Rook movement
    elif piece_type == 'R':
        if start_row == end_row:  # Horizontal move
            step = 1 if end_col > start_col else -1
            path_clear = True
            for col in range(start_col + step, end_col, step):
                if board[start_row][col] != '--':
                    path_clear = False
                    break
            move_valid = path_clear
        elif start_col == end_col:  # Vertical move
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

    # Queen movement (combination of rook and bishop)
    elif piece_type == 'Q':
        # Check if it's a valid rook move
        if start_row == end_row or start_col == end_col:
            if start_row == end_row:  # Horizontal
                step = 1 if end_col > start_col else -1
                path_clear = True
                for col in range(start_col + step, end_col, step):
                    if board[start_row][col] != '--':
                        path_clear = False
                        break
                move_valid = path_clear
            else:  # Vertical
                step = 1 if end_row > start_row else -1
                path_clear = True
                for row in range(start_row + step, end_row, step):
                    if board[row][start_col] != '--':
                        path_clear = False
                        break
                move_valid = path_clear
        # Check if it's a valid bishop move
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

    # If basic move is not valid, return False
    if not move_valid:
        return False

    # Now check if this move would leave the king in check
    # Create a temporary board to simulate the move
    temp_board = [row[:] for row in board]
    temp_board[end_row][end_col] = temp_board[start_row][start_col]
    temp_board[start_row][start_col] = '--'

    # Check if the king would be in check after this move
    if is_king_in_check(temp_board, color):
        return False

    return True

def make_move(start_row, start_col, end_row, end_col):
    global turn
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = '--'
    turn = 'b' if turn == 'w' else 'w'
    check_game_state()

def get_random_move():
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

def can_piece_attack_square(board, start_row, start_col, end_row, end_col):
    """Check if a piece can attack a square (basic movement rules only, no king safety)"""
    if start_row == end_row and start_col == end_col:
        return False

    piece = board[start_row][start_col]
    if piece == '--':
        return False

    target_piece = board[end_row][end_col]
    if target_piece != '--' and target_piece[0] == piece[0]:  # Same color
        return False

    piece_type = piece[1]

    # Pawn attack (diagonal only)
    if piece_type == 'P':
        color = piece[0]
        direction = -1 if color == 'w' else 1
        if abs(start_col - end_col) == 1 and end_row == start_row + direction:
            return True

    # Rook movement
    elif piece_type == 'R':
        if start_row == end_row:  # Horizontal move
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if board[start_row][col] != '--':
                    return False
            return True
        elif start_col == end_col:  # Vertical move
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

    # Queen movement (combination of rook and bishop)
    elif piece_type == 'Q':
        # Check if it's a valid rook move
        if start_row == end_row or start_col == end_col:
            if start_row == end_row:  # Horizontal
                step = 1 if end_col > start_col else -1
                for col in range(start_col + step, end_col, step):
                    if board[start_row][col] != '--':
                        return False
            else:  # Vertical
                step = 1 if end_row > start_row else -1
                for row in range(start_row + step, end_row, step):
                    if board[row][start_col] != '--':
                        return False
            return True
        # Check if it's a valid bishop move
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

def is_king_in_check(board, king_color):
    # Find king position
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

    # Check if any opponent piece can attack the king
    opponent_color = 'b' if king_color == 'w' else 'w'
    for row in range(8):
        for col in range(8):
            if board[row][col][0] == opponent_color:
                if can_piece_attack_square(board, row, col, king_pos[0], king_pos[1]):
                    return True
    return False

def has_legal_moves(board, color):
    for row in range(8):
        for col in range(8):
            if board[row][col][0] == color:
                for end_row in range(8):
                    for end_col in range(8):
                        if is_valid_move(row, col, end_row, end_col):
                            return True
    return False

def check_game_state():
    global game_state, winner, game_over

    white_in_check = is_king_in_check(board, 'w')
    black_in_check = is_king_in_check(board, 'b')

    white_has_moves = has_legal_moves(board, 'w')
    black_has_moves = has_legal_moves(board, 'b')

    print(f"Debug: White in check: {white_in_check}, White has moves: {white_has_moves}")
    print(f"Debug: Black in check: {black_in_check}, Black has moves: {black_has_moves}")
    print(f"Debug: Current turn: {turn}, Game over: {game_over}")

    # Only check for game end if it's actually that player's turn
    if turn == 'w':
        if not white_has_moves:
            if white_in_check:
                game_state = 'black_wins'
                winner = 'Black'
                game_over = True
                print("Debug: Black wins by checkmate!")
            else:
                game_state = 'draw'
                winner = None
                game_over = True
                print("Debug: Stalemate - Draw!")
    else:  # turn == 'b'
        if not black_has_moves:
            if black_in_check:
                game_state = 'white_wins'
                winner = 'White'
                game_over = True
                print("Debug: White wins by checkmate!")
            else:
                game_state = 'draw'
                winner = None
                game_over = True
                print("Debug: Stalemate - Draw!")

def reset_game():
    global board, selected_square, turn, game_over, winner, game_state
    # Reset board
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
    # Reset game state variables
    selected_square = None
    turn = 'w'
    game_over = False
    winner = None
    game_state = 'playing'
def draw_win_screen():
    # Create a more visible overlay with gradient effect
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)  # Even more opaque
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Add a subtle gradient background
    for i in range(HEIGHT):
        alpha = int(150 * (1 - abs(i - HEIGHT//2) / (HEIGHT//2)))
        gradient_color = (0, 0, 0, min(255, alpha))
        pygame.draw.line(screen, gradient_color, (0, i), (WIDTH, i))

    if game_state == 'white_wins':
        message = "🎉 CONGRATULATIONS! 🎉"
        sub_message = "You Won the Game!"
        color = (0, 255, 0)
        border_color = (0, 200, 0)
    elif game_state == 'black_wins':
        message = "😔 COMPUTER WINS! 😔"
        sub_message = "Better luck next time!"
        color = (255, 0, 0)
        border_color = (200, 0, 0)
    else:
        message = "🤝 IT'S A DRAW! 🤝"
        sub_message = "Well played!"
        color = (255, 255, 0)
        border_color = (200, 200, 0)

    # Main message with shadow effect
    # Shadow
    shadow_text = font.render(message, True, (0, 0, 0))
    shadow_rect = shadow_text.get_rect(center=(WIDTH//2 + 2, HEIGHT//2 - 58))
    screen.blit(shadow_text, shadow_rect)

    # Main text
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
    screen.blit(text, text_rect)

    # Sub message
    sub_text = small_font.render(sub_message, True, (255, 255, 255))
    sub_rect = sub_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
    screen.blit(sub_text, sub_rect)

    # Restart instructions with better visibility
    restart_text = small_font.render("Tap anywhere to play again", True, (220, 220, 220))
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
    screen.blit(restart_text, restart_rect)

    # Add a prominent border around the message area
    box_width = 450
    box_height = 180
    box_x = WIDTH//2 - box_width//2
    box_y = HEIGHT//2 - box_height//2

    # Outer glow effect
    for i in range(3):
        glow_color = (border_color[0]//2, border_color[1]//2, border_color[2]//2)
        pygame.draw.rect(screen, glow_color, (box_x - i, box_y - i, box_width + 2*i, box_height + 2*i), 1)

    # Main border
    pygame.draw.rect(screen, border_color, (box_x, box_y, box_width, box_height), 4)

    # Inner highlight
    pygame.draw.rect(screen, (255, 255, 255), (box_x + 2, box_y + 2, box_width - 4, box_height - 4), 1)

    print(f"WIN SCREEN: Drawing {message} with state {game_state}")

def main():
    global selected_square, turn, game_over
    clock = pygame.time.Clock()
    while True:  # Changed from while not game_over to allow restart
        for event in pygame.event.get():
            # Debug: Log all events for Pydroid3 debugging
            print(f"Pydroid3: Event type: {event.type}")
            if hasattr(event, 'type'):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(f"Pydroid3: MOUSEBUTTONDOWN - pos: {event.pos}")
                elif event.type == pygame.FINGERDOWN:
                    print(f"Pydroid3: FINGERDOWN - x: {getattr(event, 'x', 'N/A')}, y: {getattr(event, 'y', 'N/A')}, finger_id: {getattr(event, 'finger_id', 'N/A')}")
                elif event.type == pygame.MOUSEMOTION:
                    print(f"Pydroid3: MOUSEMOTION - pos: {event.pos}")
                elif event.type == pygame.FINGERMOTION:
                    print(f"Pydroid3: FINGERMOTION - x: {getattr(event, 'x', 'N/A')}, y: {getattr(event, 'y', 'N/A')}")
                elif event.type == pygame.FINGERUP:
                    print(f"Pydroid3: FINGERUP - x: {getattr(event, 'x', 'N/A')}, y: {getattr(event, 'y', 'N/A')}")

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Debug keys - declare globals first
                global game_state, winner, game_over
                # Debug: Force win with 'W' key
                if event.key == pygame.K_w:
                    game_state = 'white_wins'
                    winner = 'White'
                    game_over = True
                    print("FORCED WIN: White wins activated!")
                # Debug: Force loss with 'L' key
                elif event.key == pygame.K_l:
                    game_state = 'black_wins'
                    winner = 'Black'
                    game_over = True
                    print("FORCED LOSS: Black wins activated!")
                # Debug: Force checkmate test with 'C' key
                elif event.key == pygame.K_c:
                    # Put black king in check with no escape
                    board[0][4] = 'bK'  # Black king at a8
                    board[1][4] = 'wQ'  # White queen at a7
                    board[2][4] = 'wR'  # White rook at a6
                    print("FORCED CHECKMATE: Black king in checkmate position!")
                    check_game_state()
                # Debug: Test check detection with 'T' key
                elif event.key == pygame.K_t:
                    # Simple check test: place queen next to king
                    board[0][4] = 'bK'  # Black king at e8
                    board[0][3] = 'wQ'  # White queen at d8 (adjacent to king)
                    print("CHECK TEST: Queen adjacent to king - should show red border!")
                    # Don't call check_game_state() here as we just want to test the visual
            elif game_over:
                # Handle restart on any click/tap
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                    if event.type == pygame.FINGERDOWN:
                        # Just check if finger event occurred, don't need position for restart
                        reset_game()
                    else:
                        reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN or (is_pydroid3 and event.type not in [pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.FINGERMOTION, pygame.FINGERUP]):
                try:
                    # Pydroid3-specific touch handling
                    pos = None

                    if event.type == pygame.FINGERDOWN:
                        # Handle finger touch events for mobile - Pydroid3 compatible
                        if hasattr(event, 'x') and hasattr(event, 'y'):
                            # Pydroid3 finger coordinates are normalized (0.0 to 1.0)
                            # Convert to actual screen coordinates
                            finger_x = float(event.x)
                            finger_y = float(event.y)

                            # Ensure coordinates are within valid range
                            finger_x = max(0.0, min(1.0, finger_x))
                            finger_y = max(0.0, min(1.0, finger_y))

                            # Convert normalized coordinates to screen coordinates
                            screen_x = int(finger_x * screen_width)
                            screen_y = int(finger_y * screen_height)

                            # Adjust for window offset if the game window is smaller than screen
                            if WIDTH < screen_width:
                                screen_x = int(finger_x * WIDTH)
                            if HEIGHT < screen_height:
                                screen_y = int(finger_y * HEIGHT)

                            pos = (screen_x, screen_y)
                            print(f"Pydroid3: Finger touch at normalized ({finger_x:.3f}, {finger_y:.3f}) -> screen ({screen_x}, {screen_y})")
                        else:
                            # Fallback if finger event doesn't have proper attributes
                            print("Pydroid3: Finger event missing x/y attributes, using center")
                            pos = (WIDTH//2, HEIGHT//2)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Standard mouse click
                        pos = event.pos
                        print(f"Pydroid3: Mouse click at {pos}")
                    else:
                        # Pydroid3 might use different event types - try to get position from various attributes
                        print(f"Pydroid3: Unknown touch event type: {event.type}")
                        # Try common Pydroid3 touch attributes
                        if hasattr(event, 'pos'):
                            pos = event.pos
                            print(f"Pydroid3: Using event.pos: {pos}")
                        elif hasattr(event, 'x') and hasattr(event, 'y'):
                            # Some Pydroid3 versions might use x,y directly as screen coordinates
                            pos = (int(event.x), int(event.y))
                            print(f"Pydroid3: Using direct x,y: {pos}")
                        elif hasattr(event, 'position'):
                            pos = event.position
                            print(f"Pydroid3: Using event.position: {pos}")
                        elif hasattr(event, 'touch') and hasattr(event.touch, 'x') and hasattr(event.touch, 'y'):
                            # Some Pydroid3 versions might nest touch data
                            touch_x = float(event.touch.x)
                            touch_y = float(event.touch.y)
                            pos = (int(touch_x * WIDTH), int(touch_y * HEIGHT))
                            print(f"Pydroid3: Using nested touch: {pos}")
                        else:
                            # Try pygame touch functions as last resort
                            try:
                                if pygame.display.get_active() and pygame.touch.get_num_devices() > 0:
                                    # Get touch position using pygame's touch API
                                    touch_x, touch_y = pygame.touch.get_finger(0, 0)[:2]
                                    pos = (int(touch_x * WIDTH), int(touch_y * HEIGHT))
                                    print(f"Pydroid3: Using pygame.touch.get_finger(): {pos}")
                            except:
                                pass

                            # Last resort - use center of screen
                            if pos is None:
                                pos = (WIDTH//2, HEIGHT//2)
                                print(f"Pydroid3: No position found, using center: {pos}")

                        # Pydroid3-specific: Try to handle touch events that might be disguised as other events
                        if is_pydroid3 and pos == (WIDTH//2, HEIGHT//2):
                            # Try to get touch position from pygame mouse position as fallback
                            try:
                                mouse_pos = pygame.mouse.get_pos()
                                if mouse_pos != (0, 0):  # Only use if it's not default
                                    pos = mouse_pos
                                    print(f"Pydroid3: Using pygame.mouse.get_pos() as fallback: {pos}")
                            except:
                                pass

                    if pos is not None:
                        row, col = get_square_from_pos(pos)
                        print(f"Pydroid3: Converted to board position ({row}, {col})")

                        if row >= 0 and col >= 0:  # Valid board position
                            if selected_square is None:
                                # Select piece if it's a white piece (player's turn)
                                if board[row][col][0] == 'w':
                                    selected_square = (row, col)
                                    print(f"Pydroid3: Selected white piece at ({row}, {col})")
                                else:
                                    print(f"Pydroid3: Cannot select piece at ({row}, {col}) - not white or empty")
                            else:
                                # Try to move selected piece
                                start_row, start_col = selected_square
                                if is_valid_move(start_row, start_col, row, col):
                                    make_move(start_row, start_col, row, col)
                                    selected_square = None
                                    print(f"Pydroid3: Moved piece from ({start_row}, {start_col}) to ({row}, {col})")
                                    # Computer's turn
                                    if not game_over:
                                        move = get_random_move()
                                        if move:
                                            make_move(*move)
                                            print(f"Pydroid3: Computer moved from ({move[0]}, {move[1]}) to ({move[2]}, {move[3]})")
                                else:
                                    print(f"Pydroid3: Invalid move from ({start_row}, {start_col}) to ({row}, {col})")
                                    selected_square = None
                        else:
                            print(f"Pydroid3: Touch outside board area at screen pos {pos}")
                            selected_square = None
                    else:
                        print("Pydroid3: Could not determine touch position")

                except Exception as e:
                    print(f"Pydroid3: Touch event error: {e}")
                    import traceback
                    traceback.print_exc()
                    selected_square = None

        draw_board()
        draw_pieces()
        draw_check_indicator()
        draw_touch_feedback()  # Add visual feedback for selected pieces

        # Draw winning screen on top of everything
        if game_over:
            print(f"Game Over Screen: State={game_state}, Winner={winner}, game_over={game_over}")
            # Add a simple visual indicator
            pygame.draw.circle(screen, (255, 255, 0), (WIDTH-50, 50), 20)  # Yellow background
            pygame.draw.circle(screen, (255, 0, 0), (WIDTH-50, 50), 15)    # Red middle
            pygame.draw.circle(screen, (0, 255, 0), (WIDTH-50, 50), 10)    # Green center
            # Add text indicator
            status_font = pygame.font.SysFont('Arial', 16)
            status_text = status_font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(status_text, (WIDTH-100, 80))
            draw_win_screen()
            # Force a redraw to make sure it's visible
            pygame.display.update()

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    print("Pydroid3: Chess game starting...")
    print("Pydroid3: Touch the screen to select and move pieces!")
    print("Pydroid3: Yellow highlight shows selected piece")
    main()
