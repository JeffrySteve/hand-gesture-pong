import cv2
import numpy as np
import pygame
from .constants import CAMERA_CAPTURE_WIDTH, CAMERA_CAPTURE_HEIGHT, CAMERA_FPS

def cvimage_to_pygame(image):
    """Convert OpenCV image to Pygame Surface."""
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.rot90(image)
    surface = pygame.surfarray.make_surface(image)
    return surface

def setup_fullscreen_display():
    """Initialize pygame display in fullscreen mode."""
    pygame.init()
    infoObject = pygame.display.Info()
    WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Dual Webcam Hand Gesture Pong")
    return win, WIDTH, HEIGHT

def setup_cameras():
    """Initialize both webcam captures with better error handling and performance optimization."""
    cap0 = cv2.VideoCapture(0)
    cap1 = cv2.VideoCapture(2)
    
    # Test camera 0
    if not cap0.isOpened():
        print("Warning: Camera 0 not found, trying alternative...")
        cap0 = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Windows specific
    
    # Test camera 1 (if not available, use camera 0 for both)
    if not cap1.isOpened():
        print("Warning: Camera 1 not found, using camera 0 for both players")
        cap1 = cv2.VideoCapture(0)
    
    # Set camera properties for better performance (reduced resolution)
    for cap in [cap0, cap1]:
        if cap.isOpened():
            # Lower resolution for better performance
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_CAPTURE_WIDTH)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_CAPTURE_HEIGHT)
            cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
            
            # Additional performance optimizations
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer to minimize lag
            # Note: Auto exposure setting may not work on all cameras
            try:
                cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
            except:
                pass  # Ignore if not supported
    
    return cap0, cap1

def cleanup_resources(cap0, cap1):
    """Clean up camera and pygame resources."""
    if cap0:
        cap0.release()
    if cap1:
        cap1.release()
    cv2.destroyAllWindows()
    pygame.quit()
