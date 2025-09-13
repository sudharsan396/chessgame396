import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Get screen size for mobile compatibility
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Adjust board size based on screen with extra space for borders and title
if screen_width < 900 or screen_height < 900:
    SQUARE_SIZE = min(50, (screen_width - 100) // 8, (screen_height - 150) // 8)
else:
    SQUARE_SIZE = 60

WIDTH = SQUARE_SIZE * 8 + SQUARE_SIZE * 2  # Extra space for borders
HEIGHT = SQUARE_SIZE * 8 + SQUARE_SIZE * 2 + SQUARE_SIZE  # Extra space for title
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Enhanced colors for beautiful board
DARK_WOOD = (139, 69, 19)      # Saddle brown
LIGHT_WOOD = (222, 184, 135)   # Burlywood
BORDER_COLOR = (101, 67, 33)   # Dark brown border
HIGHLIGHT_COLOR = (255, 215, 0)  # Gold for highlights
SHADOW_COLOR = (0, 0, 0, 50)   # Semi-transparent black
TEXT_COLOR = (75, 54, 33)      # Dark brown for text

# Fonts for coordinates and title
coord_font = pygame.font.SysFont('Arial', max(12, int(SQUARE_SIZE * 0.25)))
title_font = pygame.font.SysFont('Arial', max(16, int(SQUARE_SIZE * 0.35)), bold=True)
font = pygame.font.SysFont('Arial', max(20, int(SQUARE_SIZE * 0.4)))
small_font = pygame.font.SysFont('Arial', max(14, int(SQUARE_SIZE * 0.3)))

# Piece images
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
    except:
        print(f"Could not load {file}")

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

# Fonts
font = pygame.font.SysFont('Arial', 32)
small_font = pygame.font.SysFont('Arial', 24)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

def draw_board():
    # Draw outer border with shadow effect
    border_width = int(SQUARE_SIZE * 0.1)
    board_size = SQUARE_SIZE * 8

    # Shadow
    pygame.draw.rect(screen, (0, 0, 0, 100),
                     (SQUARE_SIZE - border_width//2, SQUARE_SIZE - border_width//2,
                      board_size + border_width, board_size + border_width))

    # Main border
    pygame.draw.rect(screen, BORDER_COLOR,
                     (SQUARE_SIZE - border_width//2, SQUARE_SIZE - border_width//2,
                      board_size + border_width, board_size + border_width), border_width)

    # Inner highlight border
    pygame.draw.rect(screen, HIGHLIGHT_COLOR,
                     (SQUARE_SIZE - border_width//4, SQUARE_SIZE - border_width//4,
                      board_size + border_width//2, board_size + border_width//2), 2)

    # Draw chess squares with enhanced colors and effects
    for row in range(8):
        for col in range(8):
            x = col * SQUARE_SIZE + SQUARE_SIZE
            y = row * SQUARE_SIZE + SQUARE_SIZE

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
                for i in range(0, SQUARE_SIZE, 4):
                    alpha = 30 + (i % 20)
                    grain_color = (
                        min(255, base_color[0] + alpha),
                        min(255, base_color[1] + alpha//2),
                        min(255, base_color[2] + alpha//3)
                    )
                    pygame.draw.line(screen, grain_color, (x, y + i), (x + SQUARE_SIZE, y + i), 1)

    # Draw coordinate labels
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    numbers = ['8', '7', '6', '5', '4', '3', '2', '1']

    # Bottom letters (a-h)
    for i, letter in enumerate(letters):
        text = coord_font.render(letter, True, TEXT_COLOR)
        x = SQUARE_SIZE + i * SQUARE_SIZE + SQUARE_SIZE//2 - text.get_width()//2
        y = SQUARE_SIZE + board_size + border_width//2
        screen.blit(text, (x, y))

    # Side numbers (8-1)
    for i, number in enumerate(numbers):
        text = coord_font.render(number, True, TEXT_COLOR)
        x = SQUARE_SIZE - text.get_width() - border_width//2
        y = SQUARE_SIZE + i * SQUARE_SIZE + SQUARE_SIZE//2 - text.get_height()//2
        screen.blit(text, (x, y))

    # Draw title
    title = title_font.render("CHESS MASTER", True, HIGHLIGHT_COLOR)
    title_x = WIDTH//2 - title.get_width()//2
    title_y = SQUARE_SIZE//4
    screen.blit(title, (title_x, title_y))

def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--' and piece in images:
                img = images[piece]
                # Position pieces within the bordered board
                x = col * SQUARE_SIZE + SQUARE_SIZE + (SQUARE_SIZE - img.get_width()) // 2
                y = row * SQUARE_SIZE + SQUARE_SIZE + (SQUARE_SIZE - img.get_height()) // 2
                screen.blit(img, (x, y))

def get_square_from_pos(pos):
    x, y = pos
    # Adjust for board offset (border)
    x -= SQUARE_SIZE
    y -= SQUARE_SIZE
    if x < 0 or y < 0 or x >= SQUARE_SIZE * 8 or y >= SQUARE_SIZE * 8:
        return -1, -1  # Invalid position
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col

def is_valid_move(start_row, start_col, end_row, end_col):
    piece = board[start_row][start_col]
    if piece == '--':
        return False
    if board[end_row][end_col][0] == piece[0]:  # Same color
        return False
    # Basic movement checks (simplified)
    if piece[1] == 'P':
        direction = -1 if piece[0] == 'w' else 1
        if start_col == end_col:
            if board[end_row][end_col] == '--':
                if end_row == start_row + direction:
                    return True
                elif end_row == start_row + 2 * direction and start_row == (6 if piece[0] == 'w' else 1):
                    return True
        elif abs(start_col - end_col) == 1 and end_row == start_row + direction:
            if board[end_row][end_col] != '--':
                return True
    elif piece[1] == 'R':
        if start_row == end_row or start_col == end_col:
            return True
    elif piece[1] == 'N':
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return True
    elif piece[1] == 'B':
        if abs(start_row - end_row) == abs(start_col - end_col):
            return True
    elif piece[1] == 'Q':
        if start_row == end_row or start_col == end_col or abs(start_row - end_row) == abs(start_col - end_col):
            return True
    elif piece[1] == 'K':
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return True
    return False

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
                if is_valid_move(row, col, king_pos[0], king_pos[1]):
                    return True
    return False

def has_legal_moves(board, color):
    for row in range(8):
        for col in range(8):
            if board[row][col][0] == color:
                for end_row in range(8):
                    for end_col in range(8):
                        if is_valid_move(row, col, end_row, end_col):
                            # Make temporary move
                            temp_board = [row[:] for row in board]
                            temp_board[end_row][end_col] = temp_board[row][col]
                            temp_board[row][col] = '--'
                            # Check if king would still be in check
                            if not is_king_in_check(temp_board, color):
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

    if not white_has_moves and white_in_check:
        game_state = 'black_wins'
        winner = 'Black'
        game_over = True
        print("Debug: Black wins!")
    elif not black_has_moves and black_in_check:
        game_state = 'white_wins'
        winner = 'White'
        game_over = True
        print("Debug: White wins!")
    elif not white_has_moves and not black_has_moves:
        game_state = 'draw'
        winner = None
        game_over = True
        print("Debug: Draw!")

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
            elif game_over:
                # Handle restart on any click/tap
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                    reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                if event.type == pygame.FINGERDOWN:
                    # Convert finger position to screen coordinates
                    pos = (event.x * WIDTH, event.y * HEIGHT)
                else:
                    pos = event.pos
                row, col = get_square_from_pos(pos)
                if selected_square is None:
                    if board[row][col][0] == 'w':
                        selected_square = (row, col)
                else:
                    start_row, start_col = selected_square
                    if is_valid_move(start_row, start_col, row, col):
                        make_move(start_row, start_col, row, col)
                        selected_square = None
                        # Computer's turn
                        if not game_over:  # Only computer moves if game not over
                            move = get_random_move()
                            if move:
                                make_move(*move)
                    else:
                        selected_square = None

        draw_board()
        draw_pieces()

        # Draw winning screen on top of everything
        if game_over:
            print(f"Game Over Screen: State={game_state}, Winner={winner}, game_over={game_over}")
            # Add a simple visual indicator
            pygame.draw.circle(screen, (255, 255, 0), (WIDTH-50, 50), 20)
            pygame.draw.circle(screen, (255, 0, 0), (WIDTH-50, 50), 15)
            pygame.draw.circle(screen, (0, 255, 0), (WIDTH-50, 50), 10)
            draw_win_screen()
            # Force a redraw to make sure it's visible
            pygame.display.update()

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
