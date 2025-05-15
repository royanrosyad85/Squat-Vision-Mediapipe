# Squat Analysis using MediaPipe

A real-time AI-powered system for analyzing squat form and posture using MediaPipe pose estimation. This application offers feedback on your squat technique and evaluates pose estimation accuracy using MPJPE metrics.

## Features

### Squat Analysis
- **Real-time form detection**: Analyze squat form during a workout
- **Video upload**: Upload and analyze recorded videos
- **Feedback**: Get immediate feedback on correct/incorrect form
- **Customizable modes**: Beginner and Pro settings available

### MPJPE Evaluation
- **Mean Per Joint Position Error**: Evaluate pose estimation accuracy 
- **Joint-wise analysis**: Detailed error analysis for individual joints
- **Real-time visualization**: View error metrics during pose estimation
- **Comparison view**: Option to visualize the difference between predicted and ground truth landmarks

## Key Landmarks for MPJPE Evaluation

The MPJPE evaluation focuses on the following key landmarks:
- Shoulder (landmark_id: 11)
- Elbow (landmark_id: 13)
- Wrist (landmark_id: 15)
- Hip (landmark_id: 23)
- Knee (landmark_id: 25)
- Ankle (landmark_id: 27)
- Foot (landmark_id: 31)

## How MPJPE is Calculated

The Mean Per Joint Position Error (MPJPE) is calculated as the average Euclidean distance between the predicted joint positions and the ground truth positions:

MPJPE = (1/N) * Σ ||P_i - GT_i||_2

Where:
- N is the number of joints being evaluated
- P_i is the predicted position of joint i
- GT_i is the ground truth position of joint i
- ||.||_2 represents the Euclidean distance

## Interpreting MPJPE Values

- **< 5 pixels**: Excellent accuracy
- **5-10 pixels**: Good accuracy, suitable for most applications
- **> 10 pixels**: Needs improvement, may require better conditions or calibration

## Installation

### Requirements
- Python 3.7+
- OpenCV
- MediaPipe
- Streamlit
- NumPy

### Setup

```bash
# Clone the repository
git clone https://github.com/your-username/squat-analysis-mediapipe.git
cd squat-analysis-mediapipe

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run 🏠️_Demo.py
```

## Usage

1. Navigate to the Live Stream page to analyze your squats in real time
2. Enable MPJPE evaluation to see accuracy metrics
3. Adjust settings as needed for your experience level
4. Use the Upload Video page to analyze pre-recorded videos
5. Visit the MPJPE Analysis page to learn more about pose estimation accuracy

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for the pose estimation framework
- [Streamlit](https://streamlit.io/) for the web application framework