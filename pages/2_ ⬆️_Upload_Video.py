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


download = None

if 'download' not in st.session_state:
    st.session_state['download'] = False


output_video_file = f'output_recorded.mp4'

if os.path.exists(output_video_file):
    os.remove(output_video_file)


with st.form('Upload', clear_on_submit=True):
    up_file = st.file_uploader("Upload a Video", ['mp4','mov', 'avi'])
    uploaded = st.form_submit_button("Upload")

stframe = st.empty()

ip_vid_str = '<p style="font-family:Helvetica; font-weight: bold; font-size: 16px;">Input Video</p>'
warning_str = '<p style="font-family:Helvetica; font-weight: bold; color: Red; font-size: 17px;">Please Upload a Video first!!!</p>'

warn = st.empty()


download_button = st.empty()

if up_file and uploaded:
    
    download_button.empty()
    tfile = tempfile.NamedTemporaryFile(delete=False)

    try:
        warn.empty()
        tfile.write(up_file.read())

        vf = cv2.VideoCapture(tfile.name)

        # ---------------------  Write the processed video frame. --------------------
        fps = int(vf.get(cv2.CAP_PROP_FPS))
        width = int(vf.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vf.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_size = (width, height)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_output = cv2.VideoWriter(output_video_file, fourcc, fps, frame_size)
        # -----------------------------------------------------------------------------

        
        txt = st.sidebar.markdown(ip_vid_str, unsafe_allow_html=True)   
        ip_video = st.sidebar.video(tfile.name) 

        while vf.isOpened():
            ret, frame = vf.read()
            if not ret:
                break

            # convert frame from BGR to RGB before processing it.
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out_frame, _ = upload_process_frame.process(frame, pose)
            stframe.image(out_frame)
            video_output.write(out_frame[...,::-1])

        
        vf.release()
        video_output.release()
        
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
        txt.empty()
        tfile.close()
    
    except AttributeError:
        warn.markdown(warning_str, unsafe_allow_html=True)   



if os.path.exists(output_video_file):
    with open(output_video_file, 'rb') as op_vid:
        download = download_button.download_button('Download Video', data = op_vid, file_name='output_recorded.mp4')
    
    if download:
        st.session_state['download'] = True



if os.path.exists(output_video_file) and st.session_state['download']:
    os.remove(output_video_file)
    st.session_state['download'] = False
    download_button.empty()


    
    

    


