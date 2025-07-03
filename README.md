# Hand Gesture Pong

A modern Pong game controlled by hand gestures using computer vision and MediaPipe.

## Features
- Dual webcam support for two players
- Hand gesture controls (pinch fingers to move paddles)
- Real-time gesture detection
- Fullscreen gameplay
- Clean, modular code architecture

## Requirements
- Python 3.8+
- Two webcams (built-in + external)
- Good lighting for gesture detection

## Installation
1. Clone/download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play
1. Run the game:
   ```bash
   python main.py
   ```
2. Press SPACE to start
3. Pinch your index finger and thumb together to control your paddle
4. First to 5 points wins!

## Controls
- **Menu**: SPACE (start), Q (quit)
- **Game**: Pinch gesture to move paddle
- **Exit**: Q key anytime

## Project Structure
```
hand_gesture_pong/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── utils/                  # Utilities and constants
├── game/                   # Game logic and objects
├── ui/                     # User interface
└── assets/                 # Future assets
```

## Troubleshooting
- Ensure both webcams are connected
- Check lighting conditions for better gesture detection
- Adjust PINCH_THRESHOLD in constants.py if needed
