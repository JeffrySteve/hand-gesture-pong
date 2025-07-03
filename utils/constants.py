import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

# Game settings
BALL_SIZE = 30
BALL_SPEED = 7
BALL_SPEED_INCREASE = 0.3     # Speed increase per paddle hit
BALL_MAX_SPEED = 15           # Maximum ball speed
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 150
PADDLE_OFFSET = 50
BORDER_MARGIN = 100
WINNING_SCORE = 5

# Gesture detection
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7
PINCH_THRESHOLD = 0.07
GESTURE_MIN_REGION = 0.05  # Start at 5% from top for maximum height
GESTURE_MAX_REGION = 0.95  # End at 95% from top for maximum height
GESTURE_SIDE_MARGIN = 0.05  # 5% margin from left/right sides

# Alternative presets (comment/uncomment as needed):
# GESTURE_MIN_REGION = 0.0   # Full height option
# GESTURE_MAX_REGION = 1.0   # Full height option

# Camera settings
CAMERA_DISPLAY_WIDTH = 200    # Reduced from 240
CAMERA_DISPLAY_HEIGHT = 150   # Reduced from 180
CAMERA_BORDER_WIDTH = 3       # Reduced from 4
GESTURE_INDICATOR_SIZE = 18   # Reduced from 20

# Performance optimization
CAMERA_CAPTURE_WIDTH = 320    # Reduced from 640
CAMERA_CAPTURE_HEIGHT = 240   # Reduced from 480
CAMERA_FPS = 30

# Paddle smoothing
PADDLE_SMOOTHING_ENABLED = True
PADDLE_LERP_FACTOR = 0.3      # Increased from 0.25 for more responsiveness
MIN_GESTURE_CONFIDENCE = 0.6  # Reduced from 0.8 for better detection
GESTURE_STABILITY_FRAMES = 2  # Reduced from 3 for faster response

# UI settings
FONT_SIZE = 80
FPS = 60

# UI/UX Improvements
PADDLE_GLOW_COLOR = (100, 200, 255)
BALL_TRAIL_COLOR = (255, 255, 255, 128)
SCORE_HIGHLIGHT_COLOR = (255, 255, 0)
MENU_BUTTON_COLOR = (50, 50, 100)
MENU_BUTTON_HOVER = (80, 80, 150)
CAMERA_BORDER_ACTIVE = (0, 255, 0)
CAMERA_BORDER_INACTIVE = (255, 0, 0)

# Animation settings
PADDLE_SMOOTH_FACTOR = 0.15
BALL_TRAIL_LENGTH = 10
SCORE_FLASH_DURATION = 30
MENU_FADE_SPEED = 5
BUTTON_SCALE_FACTOR = 1.1

# Speed increase visual feedback
SPEED_FLASH_DURATION = 20     # Flash duration when speed increases
SPEED_INDICATOR_COLOR = (255, 100, 100)  # Color for speed indicator
