import os
import sys
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

BASE_DIR = os.path.abspath(os.path.join(__file__, '../../'))
sys.path.append(BASE_DIR)

from mpjpe_evaluation import calculate_mpjpe, generate_dummy_ground_truth
from utils import get_mediapipe_pose

# Set up page for compatibility with new UI
if 'statistics_analysis' not in st.session_state:
    st.session_state['statistics_analysis'] = True

# Check if we're in the main tab system or if this page was accessed directly
is_direct_access = not st.session_state.get('statistics_analysis', False)

if is_direct_access:
    st.markdown("<h1 style='text-align:center; font-family:Poppins, sans-serif;'>AI Fitness Trainer: Statistics Dashboard</h1>", unsafe_allow_html=True)
    
    # Add custom CSS for consistent styling
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        /* Main container styling */
        .main {
            background-color: #f8fafc;
            padding: 20px;
            font-family: 'Poppins', sans-serif;
        }
        
        /* Card-like styling for sections */
        .stCard {
            background-color: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 15px rgba(0,0,0,0.05);
            margin-bottom: 24px;
            border: 1px solid #f1f5f9;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        /* Chart styling */
        .stPlot > div[data-testid="stArrowVegaLiteChart"] {
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            padding: 10px;
            background-color: white;
            transition: all 0.3s ease;
        }
        
        .stPlot > div[data-testid="stArrowVegaLiteChart"]:hover {
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            transform: translateY(-5px);
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            font-family: 'Poppins', sans-serif !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #f1f5f9 !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Poppins', sans-serif !important;
        }
        
        /* Mathematic equations styling */
        .katex {
            font-size: 1.2em !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Add a container with card-like styling
st.markdown('<div class="stCard">', unsafe_allow_html=True)
st.markdown("<h2>MPJPE Analysis</h2>", unsafe_allow_html=True)

st.markdown("""
### Mean Per Joint Position Error (MPJPE)

MPJPE is a standard metric for evaluating the accuracy of human pose estimation algorithms. 
It measures the average Euclidean distance between the predicted joint positions and the ground truth positions.

This dashboard provides:
1. An explanation of MPJPE and its importance in pose estimation
2. Visualization of MPJPE for different body joints
3. Sample analysis with synthetic ground truth data
""")

# Explanation section
with st.expander("What is MPJPE?"):
    st.markdown("""
    **Mean Per Joint Position Error (MPJPE)** is calculated as:
    
    $MPJPE = \\frac{1}{N} \\sum_{i=1}^{N} ||P_i - GT_i||_2$
    
    Where:
    - $N$ is the number of joints being evaluated
    - $P_i$ is the predicted 2D or 3D position of joint $i$
    - $GT_i$ is the ground truth position of joint $i$
    - $||.||_2$ represents the Euclidean distance
    
    Lower MPJPE values indicate better pose estimation accuracy.
    
    In this application, we focus on the following joints:
    - shoulder (11)
    - elbow (13) 
    - wrist (15)
    - hip (23)
    - knee (25)
    - ankle (27)
    - foot (31)
    """)

# Sample visualization
st.header("Sample MPJPE Visualization")

tab1, tab2 = st.tabs(["Joint-wise Analysis", "Frame-by-frame Analysis"])

with tab1:
    # Create sample data for visualization
    joints = ['shoulder', 'elbow', 'wrist', 'hip', 'knee', 'ankle', 'foot']
    # Sample MPJPE values with different errors for each joint
    sample_errors = [5.2, 8.7, 10.3, 4.8, 7.2, 9.5, 6.1]
    
    # Create a bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(joints, sample_errors, color=['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'orange'])
    ax.set_xlabel('Joints')
    ax.set_ylabel('MPJPE (pixels)')
    ax.set_title('Sample MPJPE Distribution Across Different Joints')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    for i, v in enumerate(sample_errors):
        ax.text(i, v + 0.2, f"{v:.1f}", ha='center')
        
    st.pyplot(fig)
    
    st.markdown("""
    **Analysis:**
    - In this sample visualization, the wrist shows the highest error (10.3 pixels)
    - The hip shows the lowest error (4.8 pixels)
    - Extremities (wrist, ankle) typically have higher errors due to their higher mobility and occlusion challenges
    """)

with tab2:
    # Create sample data for frame-by-frame analysis
    frames = list(range(1, 101))
    
    # Generate sample MPJPE values with some variations to simulate real-world data
    np.random.seed(42)  # For reproducibility
    frame_mpjpe = 8 + 2 * np.sin(np.array(frames) / 10) + np.random.normal(0, 1, len(frames))
    
    # Create a line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(frames, frame_mpjpe, color='blue', linewidth=2)
    ax.set_xlabel('Frame Number')
    ax.set_ylabel('MPJPE (pixels)')
    ax.set_title('MPJPE Variation Across Frames')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add average line
    avg_mpjpe = np.mean(frame_mpjpe)
    ax.axhline(y=avg_mpjpe, color='r', linestyle='--', label=f'Average: {avg_mpjpe:.2f} px')
    ax.legend()
    
    st.pyplot(fig)
    
    st.markdown("""
    **Analysis:**
    - MPJPE varies frame-by-frame due to factors like motion, occlusion, and lighting
    - The cyclic pattern could indicate periodic movements like squats
    - Spikes might represent moments of rapid movement or challenging poses
    """)

# How to interpret MPJPE values
st.header("Interpreting MPJPE Values")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Excellent", "< 20 pixels", "High accuracy")
    st.markdown("Indicates excellent pose estimation with minimal error.")
with col2:
    st.metric("Good", "20-50 pixels", "Acceptable")
    st.markdown("Suitable for most applications with reasonable accuracy.")
with col3:
    st.metric("Needs Improvement", "> 50 pixels", "Higher error")
    st.markdown("May need calibration or better visibility conditions.")

# Add interactive noise level slider for testing
st.header("Test MPJPE With Different Noise Levels")
st.markdown("""
This section allows you to simulate different levels of error in pose estimation by adding 
controlled noise to landmark positions. This helps understand how MPJPE responds to different 
error magnitudes.
""")

noise_level = st.slider("Noise Level", min_value=0.0, max_value=1.0, value=0.3, step=0.1,
                       help="Higher values mean more noise (greater errors)")

if st.button("Generate Sample Landmarks With Noise"):
    # Create placeholder dictionaries for demo
    target_landmarks = {
        'shoulder': 11,
        'elbow': 13,
        'wrist': 15,
        'hip': 23,
        'knee': 25,
        'ankle': 27,
        'foot': 31
    }
    
    # Create simulated perfect prediction (just for demo purposes)
    frame_width = 640
    frame_height = 480
    perfect_prediction = {}
    
    # Simple skeleton model for demo
    # Shoulder at center top
    shoulder_x, shoulder_y = int(frame_width * 0.5), int(frame_height * 0.2)
    perfect_prediction[11] = np.array([shoulder_x, shoulder_y, 0])
    
    # Elbow below shoulder
    perfect_prediction[13] = np.array([shoulder_x, int(shoulder_y + frame_height * 0.15), 0])
    
    # Wrist below elbow
    perfect_prediction[15] = np.array([shoulder_x, int(shoulder_y + frame_height * 0.3), 0])
    
    # Hip below shoulder
    perfect_prediction[23] = np.array([shoulder_x, int(shoulder_y + frame_height * 0.25), 0])
    
    # Knee below hip
    perfect_prediction[25] = np.array([shoulder_x, int(shoulder_y + frame_height * 0.45), 0])
    
    # Ankle below knee
    perfect_prediction[27] = np.array([shoulder_x, int(shoulder_y + frame_height * 0.65), 0])
    
    # Foot slightly ahead of ankle
    perfect_prediction[31] = np.array([int(shoulder_x + frame_width * 0.05), int(shoulder_y + frame_height * 0.65), 0])
    
    # Generate "ground truth" by adding noise
    ground_truth = {}
    for joint_id, coords in perfect_prediction.items():
        # Add noise proportional to the noise_level slider
        noise_x = noise_level * (np.random.random() - 0.5) * frame_width * 0.2
        noise_y = noise_level * (np.random.random() - 0.5) * frame_height * 0.2
        noise_z = noise_level * (np.random.random() - 0.5) * 0.1
        
        ground_truth[joint_id] = np.array([coords[0] + noise_x, coords[1] + noise_y, coords[2] + noise_z])
    
    # Calculate MPJPE
    mpjpe_value, joint_errors = calculate_mpjpe(perfect_prediction, ground_truth)
    
    # Display results
    st.subheader(f"MPJPE Result: {mpjpe_value:.2f} pixels")
    
    # Display joint errors
    joint_data = []
    for joint_name, landmark_id in target_landmarks.items():
        if landmark_id in joint_errors:
            joint_data.append({
                "Joint": joint_name, 
                "Error (pixels)": round(joint_errors[joint_name], 2),
                "Assessment": "Good" if joint_errors[joint_name] < 10 else "Needs Improvement"
            })
    
    st.table(pd.DataFrame(joint_data))

# Factors affecting MPJPE
st.header("Factors Affecting MPJPE")
st.markdown("""
1. **Camera position and angle**: Non-frontal views can increase error
2. **Lighting conditions**: Poor lighting reduces landmark detection accuracy
3. **Occlusions**: When body parts are hidden or overlapping
4. **Motion blur**: Fast movements can cause blurry frames
5. **Distance from camera**: Subjects further from camera have less precise landmark detection
6. **Clothing**: Loose or unusual clothing can affect landmark detection
""")

# Sample code section
st.header("Implementation Details")
with st.expander("View MPJPE Calculation Code"):
    st.code("""
def calculate_mpjpe(prediction_landmarks, ground_truth_landmarks, target_landmarks=None):
    \"\"\"
    Calculate Mean Per Joint Position Error (MPJPE) between predicted landmarks and ground truth landmarks.
    
    Args:
        prediction_landmarks: Dictionary or array of predicted landmarks coordinates
        ground_truth_landmarks: Dictionary or array of ground truth landmarks coordinates
        target_landmarks: List of landmark indices to focus on. If None, all landmarks are evaluated.
                          Default focus on: shoulder(11), elbow(13), wrist(15), hip(23), knee(25), ankle(27), foot(31)
    
    Returns:
        mpjpe_value: Mean Per Joint Position Error
        per_joint_error: Dictionary of individual joint errors
    \"\"\"
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
""", language="python")
