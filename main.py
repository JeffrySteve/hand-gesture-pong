import pygame
import sys
from utils.helpers import setup_fullscreen_display, setup_cameras, cleanup_resources, cvimage_to_pygame
from utils.constants import *
from game.game_logic import GameLogic
from ui.hud import GameHUD
from ui.menu import Menu
from ui.components import WinnerDisplay

def main():
    # Setup
    win, WIDTH, HEIGHT = setup_fullscreen_display()
    cap0, cap1 = setup_cameras()
    
    # Check if cameras are working
    if not cap0.isOpened():
        print("Error: No camera found! Please connect at least one camera.")
        pygame.quit()
        sys.exit()
    
    clock = pygame.time.Clock()
    
    # Game components
    game_logic = GameLogic(WIDTH, HEIGHT)
    hud = GameHUD(WIDTH, HEIGHT)
    menu = Menu(WIDTH, HEIGHT)
    winner_display = WinnerDisplay(WIDTH, HEIGHT)
    
    # Game state
    game_state = "menu"  # "menu", "playing", "winner"
    running = True
    
    # Frame skipping for camera processing
    frame_skip_counter = 0
    camera_process_interval = 1  # Process camera every frame for smoother movement
    
    # UI/UX enhancement variables
    last_fps_time = pygame.time.get_ticks()
    fps_counter = 0
    current_fps = 60
    
    # Initialize camera surfaces to avoid NameError
    cam_surface0 = None
    cam_surface1 = None
    
    while running:
        clock.tick(FPS)
        events = pygame.event.get()
        
        # Calculate FPS
        fps_counter += 1
        current_time = pygame.time.get_ticks()
        if current_time - last_fps_time >= 1000:  # Update every second
            current_fps = fps_counter
            fps_counter = 0
            last_fps_time = current_time
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        if game_state == "menu":
            menu.draw(win)
            menu_action = menu.handle_events(events)
            if menu_action == "start":
                game_logic.restart_game()
                game_state = "playing"
            elif menu_action == "quit":
                running = False
                
        elif game_state == "playing":
            # Handle game controls separately
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False
            
            # Process camera feeds with optimized frequency
            frame_skip_counter += 1
            gesture1_detected = False
            gesture2_detected = False
            
            if frame_skip_counter >= camera_process_interval:
                result0, result1, frame0, frame1 = game_logic.process_cameras(cap0, cap1)
                frame_skip_counter = 0
                
                if frame0 is not None and frame1 is not None:
                    # Update paddle positions with smoothing
                    game_logic.update_paddle_positions(result0, result1)
                    
                    # Check gesture detection status
                    gesture1_detected = result0 and result0.multi_hand_landmarks is not None
                    gesture2_detected = result1 and result1.multi_hand_landmarks is not None
                    
                    # Convert camera frames for display
                    cam_surface0 = cvimage_to_pygame(frame0)
                    cam_surface1 = cvimage_to_pygame(frame1)
            else:
                # Update paddle smoothing even when not processing cameras
                game_logic.paddle1.update_smooth_movement()
                game_logic.paddle2.update_smooth_movement()
            
            # Always update ball regardless of camera processing
            game_logic.update_ball()
            
            # Update speed notifications
            game_logic.update_speed_notifications()
            
            # Check for winner
            winner = game_logic.check_game_over()
            if winner:
                winner_display.show_winner(winner)
                game_state = "winner"
            
            # Draw everything
            win.fill(BLACK)
            game_logic.paddle1.draw(win)
            game_logic.paddle2.draw(win)
            game_logic.ball.draw(win)
            
            # Draw speed notifications
            game_logic.draw_speed_notifications(win)
            
            # Update camera status and draw HUD (now with ball reference)
            hud.update_camera_status(gesture1_detected, gesture2_detected)
            hud.draw(win, game_logic.score1, game_logic.score2, cam_surface0, cam_surface1, current_fps, game_logic.ball)
            
        elif game_state == "winner":
            try:
                # Handle winner display input - only advance on SPACE press
                if winner_display.handle_input(events):
                    game_state = "menu"
                
                # Update winner display animations
                winner_display.update()
                winner_display.draw(win)
                
            except Exception as e:
                print(f"Error in winner state: {e}")
                # Fallback: return to menu
                game_state = "menu"
        
        pygame.display.update()
    
    # Cleanup
    cleanup_resources(cap0, cap1)
    sys.exit()

if __name__ == "__main__":
    main()
