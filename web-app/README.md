# Chess Master - Web Edition

🎯 **Beautiful Chess Game with AI Opponent - Play Online!**

A fully functional chess game that runs directly in your web browser using Python and Pyodide. No installation required!

## ✨ Features

- 🎮 **Full Chess Gameplay** - Complete chess rules with proper move validation
- 🤖 **AI Opponent** - Three difficulty levels (Easy, Medium, Hard)
- 📱 **Mobile Friendly** - Touch controls optimized for mobile devices
- 🎨 **Beautiful Graphics** - Wood-textured board with smooth animations
- 🔍 **Move Visualization** - See all possible moves for selected pieces
- ⚡ **PWA Support** - Install as app on mobile devices
- 🎯 **Check Indicators** - Visual warnings when king is in check
- 🏆 **Win/Lose Detection** - Proper checkmate and stalemate detection

## 🎲 How to Play

1. **Select Difficulty**: Choose Easy 🐔, Medium 🦁, or Hard 👑
2. **Make Moves**: Click/tap on your pieces to select them
3. **See Options**: Green circles show valid moves, red circles show captures
4. **Win the Game**: Checkmate the opponent's king!

### Controls
- **Desktop**: Mouse click to select and move pieces
- **Mobile**: Touch to select and move pieces
- **New Game**: Start a fresh game anytime
- **Reset**: Reset the current game
- **Fullscreen**: Maximize the game window

## 🚀 Getting Started

### Option 1: Play Online (Recommended)
Simply open `index.html` in a modern web browser!

### Option 2: Local Development
1. Clone or download the files
2. Open `index.html` in a web browser with JavaScript enabled
3. The game will automatically load Pyodide and Pygame

### Option 3: Deploy to Web
Upload all files to any web hosting service:
- Netlify (recommended)
- GitHub Pages
- Vercel
- Any static hosting

## 📱 Progressive Web App (PWA)

This game supports PWA features:
- **Install on Mobile**: Add to home screen for app-like experience
- **Offline Play**: Works without internet connection
- **Native App Feel**: Fullscreen experience on mobile devices

## 🛠️ Technical Details

- **Framework**: Pyodide (Python in the browser)
- **Graphics**: Pygame Community Edition
- **AI**: Minimax algorithm with alpha-beta pruning
- **Responsive**: Works on desktop, tablet, and mobile
- **No Server Required**: Everything runs client-side

## 🎨 Game Features

### Visual Elements
- Wood-textured chess board with gradients
- Smooth piece animations
- Check indicators with red borders
- Move path visualization
- Responsive UI for all screen sizes

### AI Intelligence
- **Easy**: Random moves
- **Medium**: Position evaluation
- **Hard**: Minimax with 2-ply lookahead

### Mobile Optimizations
- Touch-friendly interface
- Optimized piece sizes
- Responsive controls
- PWA installation support

## 🔧 Browser Requirements

- Modern web browser with JavaScript enabled
- WebAssembly support (most modern browsers)
- Recommended: Chrome, Firefox, Safari, Edge

## 📂 File Structure

```
web-app/
├── index.html          # Main HTML file
├── chess_web.py        # Python game logic
├── manifest.json       # PWA manifest
├── sw.js              # Service worker
├── *.png              # Chess piece images
└── README.md          # This file
```

## 🎮 Game Rules

Standard chess rules apply:
- Pieces move according to traditional chess rules
- Check and checkmate detection
- Stalemate detection
- Proper castling, en passant, and pawn promotion

## 🏆 Winning

- **Checkmate**: Trap the opponent's king
- **Opponent Resigns**: Force them into a losing position
- **Time**: No time limits in this version

## 🤝 Contributing

Feel free to improve the game! The code is open-source and runs entirely in the browser.

## 📄 License

MIT License - Free to use and modify!

---

**Enjoy playing Chess Master!** ♟️🤖📱