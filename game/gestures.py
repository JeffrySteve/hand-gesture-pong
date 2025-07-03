import cv2
import mediapipe as mp
from utils.constants import *

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands0 = self.mp_hands.Hands(
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
            max_num_hands=1
        )
        self.hands1 = self.mp_hands.Hands(
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
            max_num_hands=1
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Gesture stability tracking
        self.gesture_history = [[], []]  # For each player
        self.stable_positions = [None, None]  # Last stable positions
    
    def process_frame(self, frame, player_id):
        """Process camera frame and return hand landmarks."""
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        hands = self.hands0 if player_id == 0 else self.hands1
        result = hands.process(rgb)
        
        # Draw gesture detection area (the green box you see) - now larger
        h, w, _ = frame.shape
        
        # Calculate the active gesture region (larger area)
        top_margin = int(h * GESTURE_MIN_REGION)
        bottom_margin = int(h * GESTURE_MAX_REGION)
        left_margin = int(w * 0.05)  # 5% from sides (was 0.1)
        right_margin = int(w * 0.95)  # 95% to right side (was 0.9)
        
        # Draw the main detection area (green box) - thicker border for better visibility
        cv2.rectangle(frame, (left_margin, top_margin), 
                     (right_margin, bottom_margin), GREEN, 3)
        
        # Add corner markers for better visual reference
        corner_size = 20
        # Top-left corner
        cv2.line(frame, (left_margin, top_margin), (left_margin + corner_size, top_margin), GREEN, 5)
        cv2.line(frame, (left_margin, top_margin), (left_margin, top_margin + corner_size), GREEN, 5)
        
        # Top-right corner
        cv2.line(frame, (right_margin, top_margin), (right_margin - corner_size, top_margin), GREEN, 5)
        cv2.line(frame, (right_margin, top_margin), (right_margin, top_margin + corner_size), GREEN, 5)
        
        # Bottom-left corner
        cv2.line(frame, (left_margin, bottom_margin), (left_margin + corner_size, bottom_margin), GREEN, 5)
        cv2.line(frame, (left_margin, bottom_margin), (left_margin, bottom_margin - corner_size), GREEN, 5)
        
        # Bottom-right corner
        cv2.line(frame, (right_margin, bottom_margin), (right_margin - corner_size, bottom_margin), GREEN, 5)
        cv2.line(frame, (right_margin, bottom_margin), (right_margin, bottom_margin - corner_size), GREEN, 5)
        
        # Add text labels for clarity
        cv2.putText(frame, "GESTURE AREA", (left_margin + 5, top_margin - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, GREEN, 2)
        
        # Show the detection area percentage
        area_height_percent = int((GESTURE_MAX_REGION - GESTURE_MIN_REGION) * 100)
        cv2.putText(frame, f"{area_height_percent}% HEIGHT", (left_margin + 5, bottom_margin + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, GREEN, 1)
        
        # Draw additional info
        gesture_detected = result and result.multi_hand_landmarks
        status_text = "ACTIVE" if gesture_detected else "NO GESTURE"
        status_color = GREEN if gesture_detected else (0, 0, 255)  # Red if no gesture
        
        cv2.putText(frame, status_text, (10, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        return result, frame
    
    def get_paddle_position(self, hand_landmarks, screen_height, player_id):
        """Extract paddle position with stability filtering."""
        if not hand_landmarks:
            # No gesture detected, predict movement
            return self._get_predicted_position(player_id, screen_height)
        
        current_position = None
        
        for handLms in hand_landmarks:
            lm = handLms.landmark
            index_tip = lm[8]
            thumb_tip = lm[4]
            
            # Check if fingers are pinched
            distance = ((index_tip.x - thumb_tip.x) ** 2 + (index_tip.y - thumb_tip.y) ** 2) ** 0.5
            
            if distance < PINCH_THRESHOLD:
                # Use a simpler confidence check since visibility might not be available
                y_normalized = index_tip.y
                y_clamped = min(max(y_normalized, GESTURE_MIN_REGION), GESTURE_MAX_REGION)
                y_mapped = (y_clamped - GESTURE_MIN_REGION) / (GESTURE_MAX_REGION - GESTURE_MIN_REGION)
                current_position = int(y_mapped * screen_height)
                break  # Use first valid detection
        
        if current_position is not None:
            # Add to gesture history for stability checking
            self._add_to_history(player_id, current_position)
            return self._get_stable_position(player_id, current_position, screen_height)
        
        return self._get_predicted_position(player_id, screen_height)
    
    def _add_to_history(self, player_id, position):
        """Add position to gesture history."""
        history = self.gesture_history[player_id]
        history.append(position)
        
        # Keep only recent history
        if len(history) > GESTURE_STABILITY_FRAMES:
            history.pop(0)
    
    def _get_stable_position(self, player_id, current_position, screen_height):
        """Get stable position based on recent history."""
        history = self.gesture_history[player_id]
        
        if len(history) >= GESTURE_STABILITY_FRAMES:
            # Check if recent positions are stable (within reasonable range)
            avg_position = sum(history) / len(history)
            position_variance = sum((pos - avg_position) ** 2 for pos in history) / len(history)
            
            # If variance is low, use averaged position for smoother movement
            variance_threshold = (screen_height * 0.02) ** 2  # 2% of screen height variance threshold
            if position_variance < variance_threshold:
                stable_pos = int(avg_position)
                self.stable_positions[player_id] = stable_pos
                return stable_pos
        
        # Use current position if not enough history or too much variance
        self.stable_positions[player_id] = current_position
        return current_position
    
    def _get_predicted_position(self, player_id, screen_height):
        """Return predicted position when no gesture is detected."""
        if self.stable_positions[player_id] is not None:
            return self.stable_positions[player_id]
        return screen_height // 2  # Default to center
    
    def draw_landmarks(self, frame, hand_landmarks):
        """Draw hand landmarks on frame with enhanced visualization."""
        if hand_landmarks:
            for handLms in hand_landmarks:
                # Draw the hand connections
                self.mp_draw.draw_landmarks(frame, handLms, self.mp_hands.HAND_CONNECTIONS)
                
                # Highlight important landmarks (thumb tip and index tip)
                h, w, _ = frame.shape
                landmarks = handLms.landmark
                
                # Thumb tip (landmark 4)
                thumb_tip = landmarks[4]
                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                cv2.circle(frame, (thumb_x, thumb_y), 8, (255, 0, 255), -1)  # Magenta
                
                # Index finger tip (landmark 8)
                index_tip = landmarks[8]
                index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
                cv2.circle(frame, (index_x, index_y), 8, (255, 255, 0), -1)  # Cyan
                
                # Draw line between pinch points
                cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (255, 255, 255), 2)
                
                # Calculate and display pinch distance
                distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
                pinch_status = "PINCHED" if distance < PINCH_THRESHOLD else "OPEN"
                
                cv2.putText(frame, pinch_status, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
