import os
import sys
import streamlit as st
import cv2
import tempfile
import numpy as np


BASE_DIR = os.path.abspath(os.path.join(__file__, '../../'))
sys.path.append(BASE_DIR)


from utils import get_mediapipe_pose
from process_frame import ProcessFrame
from thresholds import get_thresholds_beginner, get_thresholds_pro



st.title('Fitness Vision: V-Squat Analysis')

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



upload_process_frame = ProcessFrame(thresholds=thresholds, evaluate_mpjpe=enable_mpjpe,
                                   visualize_comparison=show_comparison,
                                   display_mpjpe=display_mpjpe)

# Initialize face mesh solution
pose = get_mediapipe_pose()

# Initialize session state variables
if 'processed_frames' not in st.session_state:
    st.session_state['processed_frames'] = []
if 'video_metadata' not in st.session_state:
    st.session_state['video_metadata'] = None
if 'show_download' not in st.session_state:
    st.session_state['show_download'] = False


with st.form('Upload', clear_on_submit=True):
    up_file = st.file_uploader("Upload a Video", ['mp4','mov', 'avi'])
    uploaded = st.form_submit_button("Upload")

stframe = st.empty()

ip_vid_str = '<p style="font-family:Helvetica; font-weight: bold; font-size: 16px;">Input Video</p>'
warning_str = '<p style="font-family:Helvetica; font-weight: bold; color: Red; font-size: 17px;">Please Upload a Video first!!!</p>'

warn = st.empty()

# Placeholder for download button (will be shown after processing)
download_section = st.empty()

if up_file and uploaded:
    # Clear previous session data
    st.session_state['processed_frames'] = []
    st.session_state['video_metadata'] = None
    st.session_state['show_download'] = False
    
    tfile = tempfile.NamedTemporaryFile(delete=False)

    try:
        warn.empty()
        tfile.write(up_file.read())

        # Store video metadata for potential download
        input_filename = up_file.name
        filename_without_ext = os.path.splitext(input_filename)[0]
        
        vf = cv2.VideoCapture(tfile.name)

        # Get video properties for metadata
        fps = int(vf.get(cv2.CAP_PROP_FPS))
        width = int(vf.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vf.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Store metadata for potential video creation
        st.session_state['video_metadata'] = {
            'fps': fps,
            'width': width,
            'height': height,
            'filename': f'Result_{filename_without_ext}.mp4'
        }
        ip_video = st.sidebar.video(tfile.name) 

        while vf.isOpened():
            ret, frame = vf.read()
            if not ret:
                break

            # convert frame from BGR to RGB before processing it.
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out_frame, _ = upload_process_frame.process(frame, pose)
            stframe.image(out_frame)
            
            # Store processed frame in session state for potential download
            st.session_state['processed_frames'].append(out_frame.copy())

        
        vf.release()
        
        # Enable download option after processing is complete
        st.session_state['show_download'] = True
        
        # Show MPJPE statistics if evaluation was enabled
        if enable_mpjpe and upload_process_frame.mpjpe_values:
            st.markdown("### MPJPE Over Time")
            
            # Create a line chart with improved styling
            st.line_chart(
                upload_process_frame.mpjpe_values,
                use_container_width=True
            )
            
            # Display metrics below the chart
            col1, col2, col3 = st.columns(3)
            
            # Calculate statistics
            avg_mpjpe = np.mean(upload_process_frame.mpjpe_values)
            min_mpjpe = min(upload_process_frame.mpjpe_values) if upload_process_frame.mpjpe_values else 0
            max_mpjpe = max(upload_process_frame.mpjpe_values) if upload_process_frame.mpjpe_values else 0
            
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
        
        stframe.empty()
        ip_video.empty()
        tfile.close()
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Show download button if processing is complete
if st.session_state['show_download'] and st.session_state['processed_frames'] and st.session_state['video_metadata']:
    
    def create_video_buffer():
        """Create video file in memory buffer for direct download"""
        metadata = st.session_state['video_metadata']
        
        # Create temporary file in memory
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(
            temp_filename, 
            fourcc, 
            metadata['fps'], 
            (metadata['width'], metadata['height'])
        )
        
        # Write all frames to video
        for frame in st.session_state['processed_frames']:
            # Convert RGB back to BGR for video writing
            bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            video_writer.write(bgr_frame)
        
        video_writer.release()
        
        # Read video file as bytes for download
        with open(temp_filename, 'rb') as file:
            video_bytes = file.read()
        
        # Clean up temporary file
        os.unlink(temp_filename)
        
        return video_bytes
    
    download_section.markdown("### Download Processed Video")
    download_section.markdown("✅ **Video analysis complete!** You can now download the processed video.")
    
    # Prepare video data and show download button directly
    with st.spinner("Preparing video for download..."):
        try:
            video_data = create_video_buffer()
            
            # Show download button directly
            download_section.download_button(
                label="⬇️ Download Processed Video",
                data=video_data,
                file_name=st.session_state['video_metadata']['filename'],
                mime='video/mp4',
                key="download_video",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"❌ Error preparing video: {str(e)}")
            st.error("Please try processing the video again.")


    
    

    


