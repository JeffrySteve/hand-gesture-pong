import pygame
from .objects import Ball, Paddle
from .gestures import GestureDetector
from utils.constants import *

class GameLogic:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ball = Ball(width // 2, height // 2)
        self.paddle1 = Paddle(PADDLE_OFFSET, height // 2)
        self.paddle2 = Paddle(width - PADDLE_OFFSET - PADDLE_WIDTH, height // 2)
        self.score1 = 0
        self.score2 = 0
        self.gesture_detector = GestureDetector()
        
        # Speed tracking
        self.last_hit_count = 0
        self.speed_notifications = []
    
    def update_paddle_positions(self, result0, result1):
        """Update paddle positions based on gesture detection with smoothing."""
        pos1 = self.gesture_detector.get_paddle_position(
            result0.multi_hand_landmarks if result0 else None, self.height, 0)
        pos2 = self.gesture_detector.get_paddle_position(
            result1.multi_hand_landmarks if result1 else None, self.height, 1)
        
        if pos1 is not None:
            self.paddle1.move_to(pos1, self.height)
        else:
            self.paddle1.predict_movement()
            
        if pos2 is not None:
            self.paddle2.move_to(pos2, self.height)
        else:
            self.paddle2.predict_movement()
        
        # Apply smooth movement
        self.paddle1.update_smooth_movement()
        self.paddle2.update_smooth_movement()
    
    def update_ball(self):
        """Update ball position and handle collisions."""
        self.ball.move()
        
        # Wall collisions
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= self.height:
            self.ball.bounce_y()
        
        # Paddle collisions with speed increase
        paddle_hit = False
        if self.ball.rect.colliderect(self.paddle1.rect):
            # Only increase speed if ball is moving towards paddle
            if self.ball.speed_x < 0:
                self.ball.bounce_x()
                paddle_hit = True
        elif self.ball.rect.colliderect(self.paddle2.rect):
            # Only increase speed if ball is moving towards paddle
            if self.ball.speed_x > 0:
                self.ball.bounce_x()
                paddle_hit = True
        
        # Check for speed increase notification
        if paddle_hit and self.ball.hit_count > self.last_hit_count:
            self.last_hit_count = self.ball.hit_count
            speed_multiplier = self.ball.current_speed / self.ball.base_speed
            self.add_speed_notification(self.ball.hit_count, speed_multiplier)
        
        # Scoring
        if self.ball.rect.left <= 0:
            self.score2 += 1
            self.reset_ball()
        elif self.ball.rect.right >= self.width:
            self.score1 += 1
            self.reset_ball()
    
    def add_speed_notification(self, hit_count, speed):
        """Add speed increase notification."""
        notification = {
            'text': f"SPEED BOOST! {speed:.1f}x",
            'timer': 90,  # Show for 1.5 seconds
            'y_offset': 0,
            'alpha': 255
        }
        self.speed_notifications.append(notification)
    
    def update_speed_notifications(self):
        """Update speed notifications."""
        for notification in self.speed_notifications[:]:
            notification['timer'] -= 1
            notification['y_offset'] += 1
            notification['alpha'] = max(0, int(255 * (notification['timer'] / 90)))
            
            if notification['timer'] <= 0:
                self.speed_notifications.remove(notification)
    
    def draw_speed_notifications(self, screen):
        """Draw speed notifications."""
        font = pygame.font.SysFont('Arial', 28, bold=True)
        
        for notification in self.speed_notifications:
            text_surface = font.render(notification['text'], True, SPEED_INDICATOR_COLOR)
            text_surface.set_alpha(notification['alpha'])
            
            text_rect = text_surface.get_rect(
                center=(self.width // 2, self.height // 2 - 150 - notification['y_offset'])
            )
            screen.blit(text_surface, text_rect)
    
    def reset_ball(self):
        """Reset ball to center position and reset speed tracking."""
        self.ball.reset(self.width // 2, self.height // 2)
        self.last_hit_count = 0
        self.speed_notifications.clear()
    
    def check_game_over(self):
        """Check if game should restart and return winner."""
        try:
            if self.score1 >= WINNING_SCORE:
                return 1  # Player 1 wins
            elif self.score2 >= WINNING_SCORE:
                return 2  # Player 2 wins
            return None  # Game continues
        except Exception as e:
            print(f"Error checking game over: {e}")
            return None
    
    def restart_game(self):
        """Reset scores and ball."""
        self.score1 = 0
        self.score2 = 0
        self.reset_ball()
    
    def process_cameras(self, cap0, cap1):
        """Process both camera feeds."""
        ret0, frame0 = cap0.read()
        ret1, frame1 = cap1.read()
        
        if not ret0 or not ret1:
            return None, None, None, None
        
        result0, processed_frame0 = self.gesture_detector.process_frame(frame0, 0)
        result1, processed_frame1 = self.gesture_detector.process_frame(frame1, 1)
        
        # Draw landmarks
        self.gesture_detector.draw_landmarks(processed_frame0, result0.multi_hand_landmarks if result0 else None)
        self.gesture_detector.draw_landmarks(processed_frame1, result1.multi_hand_landmarks if result1 else None)
        
        return result0, result1, processed_frame0, processed_frame1
