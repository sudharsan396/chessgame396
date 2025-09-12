import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Get screen size for mobile compatibility
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Adjust board size based on screen
if screen_width < 800 or screen_height < 800:
    WIDTH, HEIGHT = min(600, screen_width - 20), min(600, screen_height - 20)
else:
    WIDTH, HEIGHT = 800, 800

SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)

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

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

def draw_board():
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--' and piece in images:
                img = images[piece]
                # Center the image in the square
                x = col * SQUARE_SIZE + (SQUARE_SIZE - img.get_width()) // 2
                y = row * SQUARE_SIZE + (SQUARE_SIZE - img.get_height()) // 2
                screen.blit(img, (x, y))

def get_square_from_pos(pos):
    x, y = pos
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

def main():
    global selected_square, turn, game_over
    clock = pygame.time.Clock()
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
                        move = get_random_move()
                        if move:
                            make_move(*move)
                    else:
                        selected_square = None

        draw_board()
        draw_pieces()
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
