import av
import os
import sys
import streamlit as st
from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
from aiortc.contrib.media import MediaRecorder


BASE_DIR = os.path.abspath(os.path.join(__file__, '../../'))
sys.path.append(BASE_DIR)


from utils import get_mediapipe_pose
from process_frame import ProcessFrame
from thresholds import get_thresholds_beginner, get_thresholds_pro


st.title('Live Fitness Vision : V-Squat Analysis')
st.subheader('Real-time Pose Estimation and Feedback')


# Set dark theme styling
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #262730;
        border-radius: 4px 4px 0 0;
        padding: 10px 16px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    mode = st.radio('Select Mode', ['Beginner', 'Pro'], horizontal=True)
with col2:
    enable_mpjpe = st.checkbox('Enable MPJPE Evaluation', value=False, 
                              help="Mean Per Joint Position Error - Evaluates pose estimation accuracy")

# MPJPE visualization options if MPJPE is enabled
if enable_mpjpe:
    col1_mpjpe, col2_mpjpe = st.columns(2)
    with col1_mpjpe:
        show_comparison = st.checkbox('Show Prediction vs Ground Truth', value=False,
                                    help="Visualize the difference between predicted and ground truth landmarks")
    with col2_mpjpe:
        display_mpjpe = st.checkbox('Display MPJPE on Video', value=False,
                                  help="Show MPJPE values directly on the video frame")
else:
    show_comparison = False
    display_mpjpe = False

thresholds = None 

if mode == 'Beginner':
    thresholds = get_thresholds_beginner()

elif mode == 'Pro':
    thresholds = get_thresholds_pro()


live_process_frame = ProcessFrame(thresholds=thresholds, flip_frame=True, 
                                  evaluate_mpjpe=enable_mpjpe, 
                                  visualize_comparison=show_comparison,
                                  display_mpjpe=display_mpjpe)
# Initialize face mesh solution
pose = get_mediapipe_pose()


if 'download' not in st.session_state:
    st.session_state['download'] = False

output_video_file = f'output_live.flv'

  

def video_frame_callback(frame: av.VideoFrame):
    frame = frame.to_ndarray(format="rgb24")  # Decode and get RGB frame
    frame, _ = live_process_frame.process(frame, pose)  # Process frame
    return av.VideoFrame.from_ndarray(frame, format="rgb24")  # Encode and return BGR frame


def out_recorder_factory() -> MediaRecorder:
        return MediaRecorder(output_video_file)


ctx = webrtc_streamer(
                        key="Squats-pose-analysis",
                        video_frame_callback=video_frame_callback,
                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},  # Add this config
                        media_stream_constraints={"video": {"width": {'min':480, 'ideal':480}}, "audio": False},
                        video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False),
                        out_recorder_factory=out_recorder_factory
                    )

# Display real-time MPJPE value if streaming and evaluation is enabled
if ctx.state.playing and enable_mpjpe:
    st.markdown("### MPJPE Over Time")
    
    # Display average MPJPE if we have enough values
    if len(live_process_frame.mpjpe_values) > 0:
        # Create a placeholder for the chart that updates periodically
        mpjpe_chart = st.empty()
        
        # Only show the last 100 values to avoid crowding
        display_values = live_process_frame.mpjpe_values[-100:] if len(live_process_frame.mpjpe_values) > 100 else live_process_frame.mpjpe_values
        
        # Use a line chart with improved styling
        mpjpe_chart.line_chart(
            display_values, 
            use_container_width=True
        )
        
        # Display metrics below the chart
        col1, col2, col3 = st.columns(3)
        
        # Calculate statistics
        avg_mpjpe = sum(live_process_frame.mpjpe_values) / len(live_process_frame.mpjpe_values)
        min_mpjpe = min(live_process_frame.mpjpe_values) if live_process_frame.mpjpe_values else 0
        max_mpjpe = max(live_process_frame.mpjpe_values) if live_process_frame.mpjpe_values else 0
        
        with col1:
            st.metric("Average MPJPE (px)", f"{avg_mpjpe:.2f}")
        with col2:
            st.metric("Min MPJPE (px)", f"{min_mpjpe:.2f}")
        with col3:
            st.metric("Max MPJPE (px)", f"{max_mpjpe:.2f}")
            
        # Add styling for metrics to match the desired look
        st.markdown("""
        <style>
            .stMetric {
                background-color: #262730;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .stMetric label {
                color: #FAFAFA;
            }
            .stMetric .css-1wivap2 {
                font-size: 42px;
                color: #FFFFFF;
                font-weight: bold;
            }
        </style>
        """, unsafe_allow_html=True)


download_button = st.empty()

if os.path.exists(output_video_file):
    with open(output_video_file, 'rb') as op_vid:
        download = download_button.download_button('Download Video', data = op_vid, file_name='output_live.flv')

        if download:
            st.session_state['download'] = True



if os.path.exists(output_video_file) and st.session_state['download']:
    os.remove(output_video_file)
    st.session_state['download'] = False
    download_button.empty()


    


