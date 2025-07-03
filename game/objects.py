import pygame
import random
import math
from utils.constants import *

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - BALL_SIZE // 2, y - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.base_speed = BALL_SPEED
        self.current_speed = BALL_SPEED
        self.speed_x = self.current_speed * random.choice((1, -1))
        self.speed_y = self.current_speed * random.choice((1, -1))
        self.hit_count = 0  # Track paddle hits
        self.speed_flash_timer = 0  # For visual feedback
        
        # Trail effect for speed visualization
        self.trail_positions = []
        self.max_trail_length = min(10, int(self.current_speed))
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Update trail positions
        self.trail_positions.append((self.rect.centerx, self.rect.centery))
        if len(self.trail_positions) > self.max_trail_length:
            self.trail_positions.pop(0)
        
        # Update speed flash timer
        if self.speed_flash_timer > 0:
            self.speed_flash_timer -= 1
    
    def bounce_y(self):
        self.speed_y *= -1
    
    def bounce_x(self):
        """Bounce off paddle and increase speed."""
        self.speed_x *= -1
        self.increase_speed()
    
    def increase_speed(self):
        """Increase ball speed after paddle hit."""
        self.hit_count += 1
        
        # Calculate new speed
        old_speed = self.current_speed
        self.current_speed = min(self.base_speed + (self.hit_count * BALL_SPEED_INCREASE), BALL_MAX_SPEED)
        
        # Update speed components maintaining direction
        speed_multiplier = self.current_speed / old_speed
        self.speed_x *= speed_multiplier
        self.speed_y *= speed_multiplier
        
        # Update trail length based on speed
        self.max_trail_length = min(15, int(self.current_speed * 1.5))
        
        # Trigger visual feedback
        self.speed_flash_timer = SPEED_FLASH_DURATION
        
        print(f"Ball speed increased! Hit #{self.hit_count}, Speed: {self.current_speed:.1f}")
    
    def reset(self, x, y):
        """Reset ball to center and restore base speed."""
        self.rect.center = (x, y)
        self.current_speed = self.base_speed
        self.speed_x = self.current_speed * random.choice((1, -1))
        self.speed_y = self.current_speed * random.choice((1, -1))
        self.hit_count = 0
        self.speed_flash_timer = 0
        self.trail_positions = []
        self.max_trail_length = 10
    
    def get_speed_level(self):
        """Get current speed as a percentage of max speed."""
        return (self.current_speed - self.base_speed) / (BALL_MAX_SPEED - self.base_speed)
    
    def draw(self, surface):
        # Draw speed trail
        if len(self.trail_positions) > 1:  # Ensure we have at least 2 positions
            for i, pos in enumerate(self.trail_positions[:-1]):
                alpha = int(255 * (i / len(self.trail_positions)) * 0.5)
                trail_size = max(2, int(BALL_SIZE * 0.3 * (i / len(self.trail_positions))))
                
                # Create trail surface with alpha
                trail_surface = pygame.Surface((trail_size * 2, trail_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, WHITE, (trail_size, trail_size), trail_size)
                trail_surface.set_alpha(alpha)
                surface.blit(trail_surface, (pos[0] - trail_size, pos[1] - trail_size))
        
        # Draw main ball with speed-based effects
        ball_color = WHITE
        if self.speed_flash_timer > 0:
            # Flash effect when speed increases
            flash_intensity = self.speed_flash_timer / SPEED_FLASH_DURATION
            ball_color = (
                int(255 * (1 - flash_intensity) + SPEED_INDICATOR_COLOR[0] * flash_intensity),
                int(255 * (1 - flash_intensity) + SPEED_INDICATOR_COLOR[1] * flash_intensity),
                int(255 * (1 - flash_intensity) + SPEED_INDICATOR_COLOR[2] * flash_intensity)
            )
        
        # Draw ball with speed-based glow
        if self.current_speed > self.base_speed:
            glow_size = int(BALL_SIZE + (self.current_speed - self.base_speed) * 2)
            glow_rect = pygame.Rect(
                self.rect.centerx - glow_size // 2,
                self.rect.centery - glow_size // 2,
                glow_size, glow_size
            )
            glow_color = (*SPEED_INDICATOR_COLOR, 50)
            glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surface, SPEED_INDICATOR_COLOR, (0, 0, glow_size, glow_size))
            glow_surface.set_alpha(50)
            surface.blit(glow_surface, glow_rect.topleft)
        
        # Draw main ball
        pygame.draw.ellipse(surface, ball_color, self.rect)
        
        # Draw speed indicator dots around ball
        if self.hit_count > 0:
            for i in range(min(self.hit_count, 8)):  # Max 8 dots
                angle = (i / 8) * 2 * math.pi
                dot_x = self.rect.centerx + math.cos(angle) * (BALL_SIZE // 2 + 8)
                dot_y = self.rect.centery + math.sin(angle) * (BALL_SIZE // 2 + 8)
                pygame.draw.circle(surface, SPEED_INDICATOR_COLOR, (int(dot_x), int(dot_y)), 3)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.target_y = float(y)
        self.smooth_y = float(y)
        self.last_valid_y = float(y)
        
    def move_to(self, y, screen_height):
        """Set target position for smooth movement."""
        clamped_y = max(PADDLE_HEIGHT // 2, min(y, screen_height - PADDLE_HEIGHT // 2))
        self.target_y = float(clamped_y)
        self.last_valid_y = float(clamped_y)
    
    def update_smooth_movement(self):
        """Apply smooth interpolation to paddle movement."""
        if PADDLE_SMOOTHING_ENABLED:
            # Smooth interpolation towards target
            self.smooth_y += (self.target_y - self.smooth_y) * PADDLE_LERP_FACTOR
            self.rect.centery = int(self.smooth_y)
        else:
            # Direct movement (old behavior)
            self.rect.centery = int(self.target_y)
    
    def predict_movement(self):
        """Predict next position if no gesture is detected."""
        # Keep paddle at last known good position
        self.target_y = self.last_valid_y
    
    def draw(self, surface):
        # Add subtle glow effect for better visibility
        glow_rect = pygame.Rect(self.rect.x - 2, self.rect.y - 2, 
                               self.rect.width + 4, self.rect.height + 4)
        pygame.draw.rect(surface, PADDLE_GLOW_COLOR, glow_rect, border_radius=3)
        pygame.draw.rect(surface, WHITE, self.rect, border_radius=2)
