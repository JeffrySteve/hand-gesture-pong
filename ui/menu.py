import pygame
import math
from .components import Text, MenuButton
from utils.constants import *

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.title_text = Text("Hand Gesture Pong", FONT_SIZE * 2, WHITE)
        self.subtitle_text = Text("Use hand gestures to control your paddle", FONT_SIZE // 3, LIGHT_GRAY)
        
        # Create interactive buttons
        button_width, button_height = 300, 60
        button_x = width // 2 - button_width // 2
        
        self.start_button = MenuButton("Start Game", button_x, height // 2 + 50, 
                                     button_width, button_height, "start")
        self.quit_button = MenuButton("Quit", button_x, height // 2 + 130, 
                                    button_width, button_height, "quit")
        
        self.buttons = [self.start_button, self.quit_button]
        
        # Animation variables
        self.title_float = 0
        self.background_particles = self.create_background_particles()
    
    def create_background_particles(self):
        """Create floating background particles for visual appeal."""
        import random
        particles = []
        for _ in range(30):
            particle = {
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'size': random.randint(1, 3),
                'alpha': random.randint(50, 150)
            }
            particles.append(particle)
        return particles
    
    def update_animations(self):
        """Update menu animations."""
        self.title_float += 0.05
        
        # Update background particles
        for particle in self.background_particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Wrap around screen
            if particle['x'] < 0:
                particle['x'] = self.width
            elif particle['x'] > self.width:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = self.height
            elif particle['y'] > self.height:
                particle['y'] = 0
    
    def draw(self, screen):
        """Draw the enhanced menu."""
        screen.fill(BLACK)
        
        # Draw background particles
        for particle in self.background_particles:
            color = (*WHITE, particle['alpha'])
            pygame.draw.circle(screen, WHITE, 
                             (int(particle['x']), int(particle['y'])), particle['size'])
        
        # Draw animated title
        title_y = self.height // 2 - 200 + math.sin(self.title_float) * 10
        self.title_text.draw(screen, self.width // 2, int(title_y), center=True)
        
        # Draw subtitle
        self.subtitle_text.draw(screen, self.width // 2, self.height // 2 - 100, center=True)
        
        # Draw gesture instructions
        instructions = [
            "• Pinch your index finger and thumb together",
            "• Move your hand up and down to control the paddle",
            "• Make sure you're in good lighting",
            "• First player to 5 points wins!"
        ]
        
        instruction_font = pygame.font.SysFont('Arial', 24)
        for i, instruction in enumerate(instructions):
            text_surface = instruction_font.render(instruction, True, GRAY)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 30 + i * 30))
            screen.blit(text_surface, text_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)
        
        # Update animations
        self.update_animations()
    
    def handle_events(self, events):
        """Handle menu events with mouse and keyboard support."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        # Update button states
        for button in self.buttons:
            button.update(mouse_pos)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "start"
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
        
        # Check button clicks
        if mouse_clicked:
            for button in self.buttons:
                if button.is_clicked(mouse_pos, True):
                    return button.action
        
        return None
