import numpy as np

def calculate_mpjpe(prediction_landmarks, ground_truth_landmarks, target_landmarks=None):
    """
    Calculate Mean Per Joint Position Error (MPJPE) between predicted landmarks and ground truth landmarks.
    
    Args:
        prediction_landmarks: Dictionary or array of predicted landmarks coordinates
        ground_truth_landmarks: Dictionary or array of ground truth landmarks coordinates
        target_landmarks: List of landmark indices to focus on. If None, all landmarks are evaluated.
                          Default focus on: shoulder(11), elbow(13), wrist(15), hip(23), knee(25), ankle(27), foot(31)
    
    Returns:
        mpjpe_value: Mean Per Joint Position Error
        per_joint_error: Dictionary of individual joint errors
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
    
    # Convert to numpy arrays if needed
    if isinstance(prediction_landmarks, dict) and isinstance(ground_truth_landmarks, dict):
        # Handle dictionary input format
        errors = {}
        total_error = 0
        count = 0
        
        for joint_name, landmark_id in target_landmarks.items():
            if landmark_id in prediction_landmarks and landmark_id in ground_truth_landmarks:
                pred = np.array(prediction_landmarks[landmark_id])
                gt = np.array(ground_truth_landmarks[landmark_id])
                # Calculate Euclidean distance
                error = np.linalg.norm(pred - gt)
                errors[joint_name] = error
                total_error += error
                count += 1
        
        if count == 0:
            return 0, {}
        
        mpjpe_value = total_error / count
        return mpjpe_value, errors
    
    else:
        # Handle array input format
        # Assuming both are arrays of shape [num_joints, 2 or 3]
        if isinstance(target_landmarks, dict):
            # Convert dictionary to list of indices
            target_indices = list(target_landmarks.values())
        else:
            target_indices = target_landmarks
        
        # Filter predictions and ground truth for target joints
        pred_filtered = np.array([prediction_landmarks[i] for i in target_indices if i < len(prediction_landmarks)])
        gt_filtered = np.array([ground_truth_landmarks[i] for i in target_indices if i < len(ground_truth_landmarks)])
        
        # Ensure same shape
        min_len = min(len(pred_filtered), len(gt_filtered))
        pred_filtered = pred_filtered[:min_len]
        gt_filtered = gt_filtered[:min_len]
        
        if min_len == 0:
            return 0, {}
        
        # Calculate Euclidean distance for each joint
        joint_errors = np.linalg.norm(pred_filtered - gt_filtered, axis=1)
        
        # Calculate mean error
        mpjpe_value = np.mean(joint_errors)
        
        # Create dictionary of individual joint errors
        error_dict = {}
        
        if isinstance(target_landmarks, dict):
            joint_names = list(target_landmarks.keys())
            for i, joint_name in enumerate(joint_names[:min_len]):
                error_dict[joint_name] = joint_errors[i]
        else:
            for i, landmark_id in enumerate(target_indices[:min_len]):
                error_dict[f"landmark_{landmark_id}"] = joint_errors[i]
        
        return mpjpe_value, error_dict


def format_landmark_array(landmarks, frame_width, frame_height, target_landmarks=None):
    """
    Format MediaPipe landmarks for MPJPE calculation
    
    Args:
        landmarks: MediaPipe pose landmarks
        frame_width: Width of the frame
        frame_height: Height of the frame
        target_landmarks: List of landmark indices to include
    
    Returns:
        Dictionary of landmark coordinates
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
    
    formatted_landmarks = {}
    
    for joint_name, landmark_id in target_landmarks.items():
        # Extract normalized coordinates
        x = landmarks.pose_landmarks.landmark[landmark_id].x
        y = landmarks.pose_landmarks.landmark[landmark_id].y
        z = landmarks.pose_landmarks.landmark[landmark_id].z
        
        # Convert to pixel coordinates
        pixel_x = int(x * frame_width)
        pixel_y = int(y * frame_height)
        
        # Store as array
        formatted_landmarks[landmark_id] = np.array([pixel_x, pixel_y, z])
    
    return formatted_landmarks


def generate_dummy_ground_truth(landmarks, frame_width, frame_height, noise_level=0.0):
    """
    Generate dummy ground truth landmarks for testing purposes by adding 
    small random offsets to predicted landmarks.
    
    Args:
        landmarks: MediaPipe pose landmarks
        frame_width: Width of the frame
        frame_height: Height of the frame
        noise_level: Level of noise to add (0.0-1.0)
        
    Returns:
        Dictionary of ground truth landmark coordinates
    """
    target_landmarks = {
        'shoulder': 11,
        'elbow': 13,
        'wrist': 15,
        'hip': 23,
        'knee': 25,
        'ankle': 27,
        'foot': 31
    }
    
    ground_truth = {}
    
    for joint_name, landmark_id in target_landmarks.items():
        # Extract normalized coordinates
        x = landmarks.pose_landmarks.landmark[landmark_id].x
        y = landmarks.pose_landmarks.landmark[landmark_id].y
        z = landmarks.pose_landmarks.landmark[landmark_id].z
        
        # Add small random noise to simulate ground truth data
        noise_x = noise_level * (np.random.random() - 0.5) * 0.1
        noise_y = noise_level * (np.random.random() - 0.5) * 0.1
        noise_z = noise_level * (np.random.random() - 0.5) * 0.1
        
        x_gt = x + noise_x
        y_gt = y + noise_y
        z_gt = z + noise_z
        
        # Convert to pixel coordinates
        pixel_x = int(x_gt * frame_width)
        pixel_y = int(y_gt * frame_height)
        
        # Store as array
        ground_truth[landmark_id] = np.array([pixel_x, pixel_y, z_gt])
    
    return ground_truth
