# Checkers Game with AI

A Python-based Checkers game with three difficulty levels of AI opponent, built using Tkinter.

## Features

- **Classic Checkers Gameplay**: Full implementation of standard checkers rules
- **Three AI Difficulty Levels**:
  - **Easy**: Basic moves with capture awareness
  - **Medium**: Strategic moves prioritizing captures and position
  - **Hard**: Advanced AI with sophisticated move evaluation
- **Visual Interface**: Clean, modern UI with piece graphics
- **Real-time Gameplay**: Smooth interaction with visual feedback
- **Win Condition Detection**: Automatic game end detection
- **Difficulty Switching**: Change AI difficulty during gameplay

## Game Rules

- You play as **White pieces** (bottom)
- AI plays as **Red pieces** (top)
- Regular pieces can only move forward diagonally
- Kings can move in any diagonal direction
- Captures are made by jumping over opponent pieces
- Multiple captures are allowed and mandatory
- Win by capturing all opponent pieces or blocking all moves

## Requirements

- Python 3.6 or higher
- Tkinter (usually included with Python)
- PIL (Pillow) for image handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/checkers-game.git
cd checkers-game
```

2. Install required dependencies:
```bash
pip install Pillow
```

3. Run the game:
```bash
python Start.py
```

## How to Play

1. **Start the Game**: Run `python Start.py`
2. **Select Difficulty**: Use the "Change Difficulty" button to adjust AI level
3. **Make Moves**: Click on your white pieces to select them, then click on a valid destination
4. **Captures**: Jump over red pieces to capture them
5. **Promotion**: Reach the top row to become a king
6. **Win**: Capture all red pieces or block all AI moves

## AI Difficulty Levels

### Easy
- Basic move selection
- Prioritizes captures when available
- Random choice between valid moves

### Medium
- Strategic move evaluation
- Prioritizes captures with position scoring
- Considers promotion opportunities
- Evaluates center and edge positions

### Hard
- Advanced move evaluation algorithm
- Sophisticated scoring system
- Considers multiple strategic factors
- Most challenging opponent

## File Structure

```
checkers-game/
├── Start.py              # Main entry point
├── Display.py            # GUI and window management
├── CheckersBoard.py      # Game board and piece rendering
├── AI.py                 # AI opponent implementation
├── Pieces.py             # Piece class and properties
├── PiecesMove.py         # Move validation and logic
├── PiecesState.py        # Game state management
├── resources/            # Game assets
│   ├── backGround.jpg    # Board background
│   ├── redCheckers.png   # Red piece image
│   ├── redKing.png       # Red king image
│   ├── whiteCheckers.png # White piece image
│   └── whiteKing.png     # White king image
└── README.md            # This file
```

## Controls

- **Mouse Click**: Select and move pieces
- **Change Difficulty Button**: Switch between Easy, Medium, and Hard AI
- **Close Window**: End the game

## Game Features

- **Visual Feedback**: Selected pieces are highlighted
- **Valid Move Indication**: Only valid moves are allowed
- **Capture Animation**: Visual feedback for captures
- **King Promotion**: Automatic promotion when reaching the top
- **Win Detection**: Automatic game end detection
- **Difficulty Indicator**: Shows current AI difficulty in window title

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Improving the AI algorithms
- Enhancing the UI/UX
- Adding new game modes

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with Python and Tkinter
- Checkers rules based on standard international checkers
- AI implementation using strategic evaluation algorithms 