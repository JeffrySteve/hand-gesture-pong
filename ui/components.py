import pygame
import math
import random
from utils.constants import *

class Text:
    def __init__(self, text, size=FONT_SIZE, color=WHITE):
        self.font = pygame.font.SysFont('Arial', size, bold=True)
        self.color = color
        self.original_color = color
        self.flash_timer = 0
        self.update_text(text)
    
    def update_text(self, text):
        self.text = str(text)
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()
    
    def flash(self, duration=SCORE_FLASH_DURATION):
        """Make text flash with highlight color."""
        self.flash_timer = duration
    
    def update(self):
        """Update flash animation."""
        if self.flash_timer > 0:
            self.flash_timer -= 1
            # Alternate between highlight and original color
            if self.flash_timer % 6 < 3:
                self.color = SCORE_HIGHLIGHT_COLOR
            else:
                self.color = self.original_color
            self.surface = self.font.render(self.text, True, self.color)
        else:
            self.color = self.original_color
    
    def draw(self, screen, x, y, center=False):
        if center:
            rect = self.surface.get_rect(center=(x, y))
            screen.blit(self.surface, rect)
        else:
            screen.blit(self.surface, (x, y))

class EnhancedCameraDisplay:
    def __init__(self, width=CAMERA_DISPLAY_WIDTH, height=CAMERA_DISPLAY_HEIGHT):
        self.width = width
        self.height = height
        self.border_color = CAMERA_BORDER_INACTIVE
        self.gesture_detected = False
        self.pulse_timer = 0
    
    def set_gesture_status(self, detected):
        """Update gesture detection status."""
        self.gesture_detected = detected
        self.border_color = CAMERA_BORDER_ACTIVE if detected else CAMERA_BORDER_INACTIVE
    
    def update(self):
        """Update animations."""
        self.pulse_timer += 1
    
    def draw(self, screen, surface, x, y, player_name="Player"):
        # Draw background
        bg_rect = pygame.Rect(x - 5, y - 25, self.width + 10, self.height + 35)
        pygame.draw.rect(screen, DARK_GRAY, bg_rect, border_radius=10)
        
        # Draw player label with gesture status
        label_font = pygame.font.SysFont('Arial', 20, bold=True)
        status_text = f"{player_name} {'✓' if self.gesture_detected else '✗'}"
        label_color = GREEN if self.gesture_detected else RED
        label_surface = label_font.render(status_text, True, label_color)
        label_rect = label_surface.get_rect(centerx=x + self.width // 2, y=y - 20)
        screen.blit(label_surface, label_rect)
        
        if surface:
            # Draw camera feed
            scaled_surface = pygame.transform.scale(surface, (self.width, self.height))
            screen.blit(scaled_surface, (x, y))
            
            # Draw animated border based on gesture detection
            border_width = CAMERA_BORDER_WIDTH
            if self.gesture_detected:
                # Pulsing green border for active gesture
                pulse = math.sin(self.pulse_timer * 0.3) * 0.3 + 0.7
                border_color = tuple(int(c * pulse) for c in CAMERA_BORDER_ACTIVE)
            else:
                # Steady red border for no gesture
                border_color = CAMERA_BORDER_INACTIVE
            
            pygame.draw.rect(screen, border_color, (x - border_width, y - border_width, 
                           self.width + 2 * border_width, self.height + 2 * border_width), border_width)
            
            # Draw gesture status indicator in corner
            indicator_pos = (x + self.width - 25, y + 10)
            if self.gesture_detected:
                # Green circle with checkmark
                pygame.draw.circle(screen, GREEN, indicator_pos, 12)
                pygame.draw.circle(screen, WHITE, indicator_pos, 12, 2)
                # Draw checkmark
                check_points = [(indicator_pos[0] - 6, indicator_pos[1]), 
                               (indicator_pos[0] - 2, indicator_pos[1] + 4),
                               (indicator_pos[0] + 6, indicator_pos[1] - 4)]
                pygame.draw.lines(screen, WHITE, False, check_points, 3)
            else:
                # Red circle with X
                pygame.draw.circle(screen, RED, indicator_pos, 12)
                pygame.draw.circle(screen, WHITE, indicator_pos, 12, 2)
                # Draw X
                pygame.draw.line(screen, WHITE, 
                               (indicator_pos[0] - 5, indicator_pos[1] - 5),
                               (indicator_pos[0] + 5, indicator_pos[1] + 5), 3)
                pygame.draw.line(screen, WHITE,
                               (indicator_pos[0] - 5, indicator_pos[1] + 5),
                               (indicator_pos[0] + 5, indicator_pos[1] - 5), 3)
        else:
            # No camera feed available
            no_feed_rect = pygame.Rect(x, y, self.width, self.height)
            pygame.draw.rect(screen, BLACK, no_feed_rect)
            pygame.draw.rect(screen, RED, no_feed_rect, 2)
            
            error_font = pygame.font.SysFont('Arial', 16)
            error_text = error_font.render("No Camera", True, RED)
            error_rect = error_text.get_rect(center=no_feed_rect.center)
            screen.blit(error_text, error_rect)

class MenuButton:
    def __init__(self, text, x, y, width, height, action):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.original_rect = self.rect.copy()
        self.action = action
        self.hovered = False
        self.scale = 1.0
        self.target_scale = 1.0
        self.font = pygame.font.SysFont('Arial', 32, bold=True)
    
    def update(self, mouse_pos):
        """Update button state and animations."""
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.target_scale = BUTTON_SCALE_FACTOR if self.hovered else 1.0
        
        # Smooth scaling animation
        self.scale += (self.target_scale - self.scale) * 0.2
        
        # Update rect size based on scale
        new_width = int(self.original_rect.width * self.scale)
        new_height = int(self.original_rect.height * self.scale)
        self.rect.width = new_width
        self.rect.height = new_height
        self.rect.center = self.original_rect.center
    
    def draw(self, screen):
        """Draw the button with hover effects."""
        color = MENU_BUTTON_HOVER if self.hovered else MENU_BUTTON_COLOR
        
        # Draw button background with rounded corners
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=10)
        
        # Draw button text
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos, mouse_clicked):
        """Check if button was clicked."""
        return self.rect.collidepoint(mouse_pos) and mouse_clicked

class WinnerDisplay:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.winner_text = Text("", FONT_SIZE * 2, WHITE)
        self.instruction_text = Text("Press SPACE to continue", FONT_SIZE // 2, LIGHT_GRAY)
        self.is_active = False
        self.fade_alpha = 0
        self.celebration_particles = []
        self.animation_timer = 0  # For internal animations only
    
    def show_winner(self, player_number):
        """Start displaying the winner with celebration effects."""
        try:
            self.winner_text.update_text(f"Player {player_number} Wins!")
            self.winner_text.flash(60)  # Flash for 1 second
            self.is_active = True
            self.fade_alpha = 0
            self.animation_timer = 0
            self.create_celebration_particles()
        except Exception as e:
            print(f"Error in show_winner: {e}")
            self.is_active = True  # Still show the winner screen without particles
    
    def create_celebration_particles(self):
        """Create celebration particle effects."""
        try:
            self.celebration_particles = []
            for _ in range(50):
                particle = {
                    'x': float(random.randint(0, self.width)),
                    'y': float(random.randint(0, self.height)),
                    'vx': random.uniform(-5, 5),
                    'vy': random.uniform(-5, 5),
                    'color': random.choice([YELLOW, GREEN, BLUE, WHITE]),
                    'life': random.randint(60, 120),
                    'max_life': 120  # Fixed max life instead of random
                }
                self.celebration_particles.append(particle)
        except Exception as e:
            print(f"Error creating particles: {e}")
            self.celebration_particles = []  # Ensure it's at least an empty list
    
    def update(self):
        """Update animations but don't auto-close."""
        if not self.is_active:
            return True
            
        try:
            self.animation_timer += 1
            self.fade_alpha = min(255, self.fade_alpha + 5)
            
            # Update winner text flash
            self.winner_text.update()
            
            # Update celebration particles - with better error handling
            particles_to_remove = []
            for i, particle in enumerate(self.celebration_particles):
                try:
                    particle['x'] += particle['vx']
                    particle['y'] += particle['vy']
                    particle['life'] -= 1
                    
                    # Wrap around screen edges for continuous effect
                    if particle['x'] < 0:
                        particle['x'] = self.width
                    elif particle['x'] > self.width:
                        particle['x'] = 0
                    if particle['y'] < 0:
                        particle['y'] = self.height
                    elif particle['y'] > self.height:
                        particle['y'] = 0
                    
                    # Reset particle when it dies for continuous celebration
                    if particle['life'] <= 0:
                        particle['life'] = particle['max_life']
                        particle['x'] = float(random.randint(0, self.width))
                        particle['y'] = float(random.randint(0, self.height))
                        particle['vx'] = random.uniform(-5, 5)
                        particle['vy'] = random.uniform(-5, 5)
                        
                except Exception as e:
                    print(f"Error updating particle {i}: {e}")
                    particles_to_remove.append(i)
            
            # Remove problematic particles
            for i in reversed(particles_to_remove):
                if i < len(self.celebration_particles):
                    self.celebration_particles.pop(i)
            
            # Make instruction text blink to draw attention
            if (self.animation_timer // 30) % 2 == 0:  # Blink every 0.5 seconds
                self.instruction_text.color = WHITE
            else:
                self.instruction_text.color = LIGHT_GRAY
            
            return False  # Never auto-close
            
        except Exception as e:
            print(f"Error in winner display update: {e}")
            return False
    
    def handle_input(self, events):
        """Handle input events for the winner display."""
        try:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.close()
                    return True  # Indicate that we should transition to menu
            return False
        except Exception as e:
            print(f"Error handling winner display input: {e}")
            return False
    
    def close(self):
        """Close the winner display."""
        try:
            self.is_active = False
            self.celebration_particles.clear()
            self.animation_timer = 0
        except Exception as e:
            print(f"Error closing winner display: {e}")
    
    def draw(self, screen):
        """Draw the winner screen with effects."""
        if not self.is_active:
            return False
            
        try:
            # Semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(min(180, self.fade_alpha))
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # Draw celebration particles with error handling
            for particle in self.celebration_particles:
                try:
                    if particle['max_life'] > 0:  # Prevent division by zero
                        alpha = int(255 * (particle['life'] / particle['max_life']))
                        if alpha > 0:  # Only draw visible particles
                            pygame.draw.circle(screen, particle['color'], 
                                             (int(particle['x']), int(particle['y'])), 3)
                except Exception as e:
                    print(f"Error drawing particle: {e}")
                    continue
            
            # Draw winner text
            self.winner_text.draw(screen, self.width // 2, self.height // 2 - 50, center=True)
            
            # Draw blinking instruction text
            self.instruction_text.draw(screen, self.width // 2, self.height // 2 + 50, center=True)
            
            return True
            
        except Exception as e:
            print(f"Error drawing winner screen: {e}")
            # Still try to draw basic text
            try:
                self.winner_text.draw(screen, self.width // 2, self.height // 2 - 50, center=True)
                self.instruction_text.draw(screen, self.width // 2, self.height // 2 + 50, center=True)
            except:
                pass
            return True

class SpeedNotification:
    """Display speed increase notifications."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.notifications = []
    
    def add_speed_notification(self, hit_count, speed):
        """Add a speed increase notification."""
        notification = {
            'text': f"SPEED UP! {speed:.1f}x",
            'timer': 60,  # Show for 1 second at 60 FPS
            'y_offset': 0,
            'alpha': 255
        }
        self.notifications.append(notification)
    
    def update(self):
        """Update all notifications."""
        for notification in self.notifications[:]:
            notification['timer'] -= 1
            notification['y_offset'] += 2  # Move up
            notification['alpha'] = max(0, int(255 * (notification['timer'] / 60)))
            
            if notification['timer'] <= 0:
                self.notifications.remove(notification)
    
    def draw(self, screen):
        """Draw all active notifications."""
        font = pygame.font.SysFont('Arial', 32, bold=True)
        
        for notification in self.notifications:
            text_surface = font.render(notification['text'], True, SPEED_INDICATOR_COLOR)
            text_surface.set_alpha(notification['alpha'])
            
            text_rect = text_surface.get_rect(
                center=(self.width // 2, self.height // 2 - 100 - notification['y_offset'])
            )
            screen.blit(text_surface, text_rect)
