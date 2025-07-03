import pygame
import math
from .components import Text, EnhancedCameraDisplay
from utils.constants import *

class GameHUD:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score1_text = Text("0", FONT_SIZE * 2, WHITE)
        self.score2_text = Text("0", FONT_SIZE * 2, WHITE)
        self.separator_text = Text(":", FONT_SIZE * 2, GRAY)
        
        self.camera_display1 = EnhancedCameraDisplay()
        self.camera_display2 = EnhancedCameraDisplay()
        
        # Status indicators
        self.status_font = pygame.font.SysFont('Arial', 20, bold=True)
        self.fps_display = Text("FPS: 60", 24, GREEN)
        self.speed_display = Text("SPEED: 1.0x", 24, WHITE)
        
        # Animation variables
        self.score_pulse = [0, 0]  # For each player
        
    def update_scores(self, score1, score2):
        """Update scores with flash animation on change."""
        # Check if scores changed
        if str(score1) != self.score1_text.text:
            self.score1_text.update_text(score1)
            self.score1_text.flash()
            self.score_pulse[0] = 30  # Pulse animation
        
        if str(score2) != self.score2_text.text:
            self.score2_text.update_text(score2)
            self.score2_text.flash()
            self.score_pulse[1] = 30  # Pulse animation
    
    def update_camera_status(self, gesture1_detected, gesture2_detected):
        """Update camera displays with gesture detection status."""
        self.camera_display1.set_gesture_status(gesture1_detected)
        self.camera_display2.set_gesture_status(gesture2_detected)
    
    def update_fps(self, fps):
        """Update FPS display with color coding."""
        color = GREEN if fps >= 50 else YELLOW if fps >= 30 else RED
        self.fps_display = Text(f"FPS: {int(fps)}", 24, color)
    
    def update_speed_display(self, ball):
        """Update speed display based on ball speed."""
        speed_multiplier = ball.current_speed / ball.base_speed
        color = WHITE
        
        # Color code based on speed level
        if speed_multiplier >= 1.8:
            color = RED
        elif speed_multiplier >= 1.4:
            color = YELLOW
        elif speed_multiplier >= 1.1:
            color = GREEN
        
        self.speed_display = Text(f"SPEED: {speed_multiplier:.1f}x", 24, color)
    
    def update_animations(self):
        """Update HUD animations."""
        self.score1_text.update()
        self.score2_text.update()
        self.camera_display1.update()
        self.camera_display2.update()
        
        # Update score pulse
        for i in range(2):
            if self.score_pulse[i] > 0:
                self.score_pulse[i] -= 1
    
    def draw_speed_meter(self, screen, ball):
        """Draw a visual speed meter."""
        meter_x = self.width // 2 - 100
        meter_y = 100
        meter_width = 200
        meter_height = 8
        
        # Background bar
        bg_rect = pygame.Rect(meter_x, meter_y, meter_width, meter_height)
        pygame.draw.rect(screen, DARK_GRAY, bg_rect, border_radius=4)
        
        # Speed fill
        speed_percent = (ball.current_speed - ball.base_speed) / (BALL_MAX_SPEED - ball.base_speed)
        fill_width = int(meter_width * speed_percent)
        
        if fill_width > 0:
            fill_rect = pygame.Rect(meter_x, meter_y, fill_width, meter_height)
            # Color gradient based on speed
            if speed_percent >= 0.8:
                fill_color = RED
            elif speed_percent >= 0.5:
                fill_color = YELLOW
            else:
                fill_color = GREEN
            
            pygame.draw.rect(screen, fill_color, fill_rect, border_radius=4)
        
        # Border
        pygame.draw.rect(screen, WHITE, bg_rect, 2, border_radius=4)
        
        # Labels
        speed_label = pygame.font.SysFont('Arial', 16, bold=True).render("SPEED", True, WHITE)
        screen.blit(speed_label, (meter_x, meter_y - 20))
        
        # Hit count indicator
        hit_text = pygame.font.SysFont('Arial', 14).render(f"Hits: {ball.hit_count}", True, LIGHT_GRAY)
        screen.blit(hit_text, (meter_x + meter_width - 50, meter_y - 20))
    
    def draw(self, screen, score1, score2, cam_surface0, cam_surface1, fps=60, ball=None):
        """Draw the enhanced HUD with speed indicators."""
        # Update scores and displays
        self.update_scores(score1, score2)
        self.update_fps(fps)
        if ball:
            self.update_speed_display(ball)
        self.update_animations()
        
        # Draw center line with subtle animation
        line_alpha = int(128 + math.sin(pygame.time.get_ticks() * 0.001) * 30)
        center_surface = pygame.Surface((2, self.height))
        center_surface.set_alpha(line_alpha)
        center_surface.fill(WHITE)
        screen.blit(center_surface, (self.width // 2 - 1, 0))
        
        # Draw scores with pulse effect
        score_y = 50
        
        # Player 1 score (left side)
        scale1 = 1.0 + (self.score_pulse[0] / 30.0) * 0.3 if self.score_pulse[0] > 0 else 1.0
        if scale1 > 1.0:
            score1_surface = pygame.transform.scale(self.score1_text.surface, 
                                                   (int(self.score1_text.surface.get_width() * scale1),
                                                    int(self.score1_text.surface.get_height() * scale1)))
            score1_rect = score1_surface.get_rect(center=(self.width // 2 - 80, score_y))
            screen.blit(score1_surface, score1_rect)
        else:
            self.score1_text.draw(screen, self.width // 2 - 80, score_y, center=True)
        
        # Separator
        self.separator_text.draw(screen, self.width // 2, score_y, center=True)
        
        # Player 2 score (right side)
        scale2 = 1.0 + (self.score_pulse[1] / 30.0) * 0.3 if self.score_pulse[1] > 0 else 1.0
        if scale2 > 1.0:
            score2_surface = pygame.transform.scale(self.score2_text.surface, 
                                                   (int(self.score2_text.surface.get_width() * scale2),
                                                    int(self.score2_text.surface.get_height() * scale2)))
            score2_rect = score2_surface.get_rect(center=(self.width // 2 + 80, score_y))
            screen.blit(score2_surface, score2_rect)
        else:
            self.score2_text.draw(screen, self.width // 2 + 80, score_y, center=True)
        
        # Draw speed meter (this was missing!)
        if ball:
            self.draw_speed_meter(screen, ball)
        
        # Draw camera feeds positioned away from paddle areas
        # Player 1 camera - top center-left (away from left paddle)
        cam1_x = self.width // 4 - CAMERA_DISPLAY_WIDTH // 2
        cam1_y = 130  # Below scores, above paddle area
        
        # Player 2 camera - top center-right (away from right paddle)  
        cam2_x = (self.width * 3) // 4 - CAMERA_DISPLAY_WIDTH // 2
        cam2_y = 130  # Below scores, above paddle area
        
        self.camera_display1.draw(screen, cam_surface0, cam1_x, cam1_y, "Player 1")
        self.camera_display2.draw(screen, cam_surface1, cam2_x, cam2_y, "Player 2")
        
        # Draw game status information
        status_y = self.height - 40
        
        # FPS counter
        self.fps_display.draw(screen, 20, status_y)
        
        # Speed display
        if ball:
            self.speed_display.draw(screen, 150, status_y)
        
        # Game instructions with speed info
        instruction_text = self.status_font.render("Pinch fingers to move paddle • Ball speeds up on hits • Q to quit", True, GRAY)
        instruction_rect = instruction_text.get_rect(center=(self.width // 2, status_y))
        screen.blit(instruction_text, instruction_rect)
        
        # Winning score indicator
        winning_text = self.status_font.render(f"First to {WINNING_SCORE} wins!", True, YELLOW)
        winning_rect = winning_text.get_rect(right=self.width - 20, y=status_y)
        screen.blit(winning_text, winning_rect)
