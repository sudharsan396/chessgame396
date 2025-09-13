# Chess Game in Pygame

A simple chess game built with Python and Pygame, featuring user vs computer gameplay.

## Features

- Full chess board with standard piece movements
- User plays as white pieces, computer as black
- Random AI for computer moves
- Visual chess piece images
- Mouse-based piece selection and movement

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/sudharsan396/chessgame396.git
   cd chessgame396
   ```

2. Install Pygame:
   ```
   pip install pygame
   ```

## How to Run

Run the game with:
```
python chess.py
```

- Click on a piece to select it
- Click on a destination square to move
- The computer will make its move automatically

## Game Rules

- Standard chess rules apply
- User controls white pieces
- Computer controls black pieces with random moves
- The game continues until you close the window

## Mobile Testing

This chess game is fully optimized for mobile devices! You can test it on your phone using:

### For Pydroid3 (Android):
1. Download the repository files to your mobile device
2. Open Pydroid3 app
3. Load the `chess.py` file
4. Run the game - it will automatically detect your screen size and center the board perfectly

### Features for Mobile:
- ✅ Responsive board sizing (adapts to any screen size)
- ✅ Perfect centering on any device
- ✅ Touch controls optimized for fingers
- ✅ Fullscreen mode support
- ✅ Mobile-specific error handling
- ✅ Visual check indicators
- ✅ Winning screen with restart functionality

### Mobile Controls:
- Tap a piece to select it
- Tap destination square to move
- Tap anywhere on winning screen to restart
- Use debug keys (W/L/C/T) for testing (if keyboard available)

## Files

- `chess.py` - Main game code
- `w*.png` - White piece images
- `b*.png` - Black piece images

## Future Improvements

- Better AI algorithm (minimax, etc.)
- Check/checkmate detection
- Castling, en passant, promotion
- Game save/load
- Multiplayer mode

## License

This project is open source and available under the [MIT License](LICENSE).

Enjoy playing chess!
