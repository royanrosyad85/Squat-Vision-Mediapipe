import streamlit as st

st.set_page_config(page_title="Squat Vision", page_icon="🏋️", layout="centered")

st.title('Squat Vision: Analyze Your Squat Technique')
st.markdown("---")
st.markdown("""
### Overview
Squat Vision adalah aplikasi AI yang membantu Anda menganalisis teknik squat secara real-time maupun dari video rekaman. Dengan teknologi pose estimation (MediaPipe), aplikasi ini memberikan feedback langsung mengenai postur squat Anda dan mengevaluasi akurasi deteksi pose menggunakan metrik MPJPE (Mean Per Joint Position Error).

**Fitur utama:**
- Analisis squat secara real-time melalui webcam
- Upload video untuk analisis postur squat
- Evaluasi akurasi pose estimation dengan MPJPE
- Mode Beginner & Pro sesuai kebutuhan
- Visualisasi perbedaan prediksi dan ground truth
""")

st.markdown("""
### Cara Menggunakan
1. Pilih menu **Live Stream** untuk analisis squat secara langsung menggunakan webcam.
2. Pilih menu **Upload Video** untuk menganalisis video squat yang sudah direkam.
3. Aktifkan fitur MPJPE untuk melihat evaluasi akurasi pose estimation.
4. Kunjungi halaman **MPJPE Analysis** untuk memahami lebih lanjut tentang metrik evaluasi dan interpretasinya.
""")

st.markdown("""
## Quick Navigation
""")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button('📷️ Live Stream'):
        st.switch_page('pages/1_📷️_Live_Stream.py')
with col2:
    if st.button('📂 Upload Video'):
        st.switch_page('pages/2_ ⬆️_Upload_Video.py')
with col3:
    if st.button('📊 MPJPE Analysis'):
        st.switch_page('pages/3_📊_MPJPE_Analysis.py')

st.markdown("""
---

<sub>Squat Vision is developed using Mediapipe and OpenCV.</sub>
""", unsafe_allow_html=True)









