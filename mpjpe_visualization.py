import cv2
import numpy as np

def draw_mpjpe_results(frame, mpjpe_value, joint_errors, position=(30, 60), 
                      overall_color=(0, 255, 0), joint_colors=None, font_scale=0.6,
                      add_background=True):
    """
    Draw MPJPE evaluation results on the frame
    
    Args:
        frame: OpenCV image frame
        mpjpe_value: Overall MPJPE value
        joint_errors: Dictionary of individual joint errors
        position: Starting position (x, y) for drawing
        overall_color: Color for overall MPJPE value
        joint_colors: Dictionary of colors for each joint
        font_scale: Font scale for text
        add_background: Whether to add a semi-transparent background behind text
    
    Returns:
        Frame with MPJPE visualization
    """
    # Create a copy of the frame
    result_frame = frame.copy()
    
    # Set default colors if not provided
    if joint_colors is None:
        joint_colors = {
            'shoulder': (255, 0, 0),      # Blue
            'elbow': (0, 255, 0),         # Green
            'wrist': (0, 0, 255),         # Red
            'hip': (255, 255, 0),         # Cyan
            'knee': (255, 0, 255),        # Magenta
            'ankle': (0, 255, 255),       # Yellow
            'foot': (255, 165, 0)         # Orange
        }
    
    x, y = position
    
    # Calculate dynamic color for each joint based on error value
    dynamic_colors = {}
    for joint_name, error in joint_errors.items():
        # Set color based on error (green->yellow->red gradient)
        if error < 5:  # Low error
            dynamic_colors[joint_name] = (0, 255, 0)  # Green
        elif error < 10:  # Medium error
            dynamic_colors[joint_name] = (0, 255, 255)  # Yellow
        else:  # High error
            dynamic_colors[joint_name] = (0, 0, 255)  # Red
    
    # Draw overall MPJPE value with background
    text = f"MPJPE: {mpjpe_value:.2f} px"
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
    
    # Add semi-transparent background for better readability
    if add_background:
        # Panel for all text
        panel_height = text_size[1] + (len(joint_errors) * 30) + 10
        panel_width = max(text_size[0], 200) + 20
        
        overlay = result_frame.copy()
        cv2.rectangle(overlay, (x-5, y-text_size[1]-5), 
                     (x+panel_width, y+panel_height), 
                     (0, 0, 0), -1)
        # Apply overlay with transparency
        alpha = 0.6
        cv2.addWeighted(overlay, alpha, result_frame, 1-alpha, 0, result_frame)
    
    # Draw overall MPJPE value
    cv2.putText(result_frame, text, (x, y), 
                cv2.FONT_HERSHEY_SIMPLEX, font_scale, overall_color, 2)
    
    # Draw individual joint errors with dynamic coloring
    y_offset = 30
    for i, (joint_name, error) in enumerate(joint_errors.items()):
        # Use dynamic color based on error value
        joint_color = dynamic_colors.get(joint_name, (255, 255, 255))
        
        cv2.putText(result_frame, f"{joint_name}: {error:.2f} px", 
                   (x, y + (i+1)*y_offset), cv2.FONT_HERSHEY_SIMPLEX, 
                   font_scale, joint_color, 1)
    
    return result_frame


def visualize_mpjpe_comparison(frame, prediction_landmarks, ground_truth_landmarks, 
                              target_landmarks=None, line_color=(0, 0, 255), line_thickness=2):
    """
    Visualize the difference between predicted landmarks and ground truth landmarks
    
    Args:
        frame: OpenCV image frame
        prediction_landmarks: Dictionary of predicted landmark coordinates
        ground_truth_landmarks: Dictionary of ground truth landmark coordinates
        target_landmarks: Dictionary or list of target landmark indices
        line_color: Color for the error lines
        line_thickness: Thickness for the error lines
    
    Returns:
        Frame with visualization of prediction errors
    """
    if target_landmarks is None:
        target_landmarks = {
            'shoulder': 11,
            'elbow': 13,
            'wrist': 15,
            'hip': 23,
            'knee': 25,
            'ankle': 27,
            'foot': 31
        }
    
    # Create a copy of the frame
    result_frame = frame.copy()
    
    # Draw lines between predicted and ground truth landmarks
    for joint_name, landmark_id in target_landmarks.items():
        if landmark_id in prediction_landmarks and landmark_id in ground_truth_landmarks:
            # Get pixel coordinates
            pred = prediction_landmarks[landmark_id]
            gt = ground_truth_landmarks[landmark_id]
            
            pred_point = (int(pred[0]), int(pred[1]))
            gt_point = (int(gt[0]), int(gt[1]))
            
            # Draw line connecting prediction and ground truth
            cv2.line(result_frame, pred_point, gt_point, line_color, line_thickness)
            
            # Draw circles at both points
            cv2.circle(result_frame, pred_point, 5, (0, 255, 0), -1)  # Green for prediction
            cv2.circle(result_frame, gt_point, 5, (255, 0, 0), -1)    # Red for ground truth
    
    return result_frame
