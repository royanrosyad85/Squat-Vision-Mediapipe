import streamlit as st

st.set_page_config(page_title="Fitness Vision", page_icon="🏋️", layout="centered")

st.title('Fitness Vision: Analyze Your Squat Technique')
st.markdown("---")

# Add system requirements section with improved organization
st.markdown("""
### 📋 System Requirements & Setup Guidelines

> **Penting**: Ikuti panduan berikut untuk mendapatkan hasil analisis pose yang optimal dan akurat
""")

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["📹 Video & Camera", "💡 Lighting & Environment", "👤 Positioning & Setup"])

with tab1:
    st.markdown("""
    #### 📹 Spesifikasi Video & Kamera
    
    **Format Video yang Didukung:**
    - **Format file**: MP4, MOV, AVI
    - **Resolusi minimum**: 480p (640x480)
    - **Resolusi optimal**: 720p (1280x720) atau 1080p (1920x1080)
    - **Frame rate**: 15-30 FPS (24-30 FPS direkomendasikan)
    - **Durasi maksimal**: 5 menit per video
    - **Orientasi**: Landscape/horizontal (16:9 atau 4:3)
    
    **Spesifikasi Kamera:**
    - **Resolusi webcam**: Minimum 720p untuk live stream
    - **Stabilitas**: Gunakan tripod atau holder yang stabil
    - **Fokus**: Auto-focus atau manual focus yang tajam
    - **Codec**: H.264 untuk kompatibilitas terbaik
    """)

with tab2:
    st.markdown("""
    #### 💡 Kondisi Pencahayaan & Lingkungan
    
    **Pencahayaan Optimal:**
    - **Intensitas**: Terang dan merata di seluruh area
    - **Arah cahaya**: Cahaya dari depan atau samping, hindari backlight
    - **Bayangan**: Minimal atau tidak ada bayangan pada tubuh
    - **Kontras**: Background kontras dengan warna kulit/pakaian
    - **Konsistensi**: Pencahayaan stabil selama rekaman
    
    **Pengaturan Lingkungan:**
    - **Background**: Polos, warna solid (putih, abu-abu, atau biru)
    - **Ruang**: Area kosong minimal 2x2 meter
    - **Gangguan**: Tidak ada objek bergerak di background
    - **Refleksi**: Hindari permukaan reflektif atau cermin
    """)

with tab3:
    st.markdown("""
    #### � Posisi Kamera & Area Deteksi
    
    **Setup Kamera:**
    - **Ketinggian**: Sejajar dengan pinggang/pusat tubuh
    - **Jarak**: 2-3 meter dari subjek
    - **Sudut**: Posisi samping (side view) untuk analisis squat terbaik
    - **Stabilitas**: Kamera tetap, tidak bergerak selama rekaman
    
    **Area Tubuh yang Wajib Terlihat:**
    - ✅ **Kepala** hingga **kaki** (full body)
    - ✅ **Joint penting**: Bahu, siku, pergelangan tangan, pinggul, lutut, pergelangan kaki
    - ✅ **Ruang kosong**: 20-30cm di atas kepala dan bawah kaki
    - ✅ **Tidak terpotong**: Semua ekstremitas terlihat lengkap
    
    **Pakaian yang Direkomendasikan:**
    - **Ideal**: Athletic wear atau pakaian ketat
    - **Warna**: Kontras dengan background
    - **Hindari**: Pakaian longgar, bermotif rumit, atau reflektif
    """)

# Add visual comparison guide
st.markdown("""
### 📖 Panduan Visual: Do's & Don'ts

""")

col_do, col_dont = st.columns(2)

with col_do:
    st.success("""
    **✅ SETUP YANG BENAR:**
    - Background polos dan kontras
    - Pencahayaan merata dari depan/samping
    - Seluruh tubuh terlihat dalam frame
    - Pakaian athletic wear yang pas
    - Kamera stabil di posisi samping
    - Satu orang dalam frame
    - Ruang gerak yang cukup
    - Joint landmarks jelas terlihat
    """)

with col_dont:
    st.error("""
    **❌ HINDARI:**
    - Background ramai atau berpola
    - Backlight atau silhouette
    - Tubuh terpotong atau tersembunyi
    - Pakaian longgar yang menutupi joint
    - Kamera bergerak atau tidak stabil
    - Multiple orang dalam frame
    - Gerakan terlalu cepat
    - Oklusi atau objek penghalang
    """)

st.markdown("---")

st.markdown("""
### Overview
Fitness Vision adalah aplikasi AI yang membantu Anda menganalisis teknik squat secara real-time maupun dari video rekaman. Dengan teknologi pose estimation (MediaPipe), aplikasi ini memberikan feedback langsung mengenai postur squat Anda dan mengevaluasi akurasi deteksi pose menggunakan metrik MPJPE (Mean Per Joint Position Error).

**Fitur utama:**
- Analisis squat secara real-time melalui webcam
- Upload video untuk analisis postur squat
- Evaluasi akurasi pose estimation dengan MPJPE
- Mode Beginner & Pro sesuai kebutuhan
- Visualisasi perbedaan prediksi dan ground truth
""")

st.markdown("""
### Cara Menggunakan
1. **Setup Environment**: Pastikan spesifikasi di atas terpenuhi
2. Pilih menu **Live Stream** untuk analisis squat secara langsung menggunakan webcam
3. Pilih menu **Upload Video** untuk menganalisis video squat yang sudah direkam
4. Aktifkan fitur MPJPE untuk melihat evaluasi akurasi pose estimation
5. Kunjungi halaman **MPJPE Analysis** untuk memahami lebih lanjut tentang metrik evaluasi
""")

# Add comprehensive troubleshooting section
with st.expander("🔧 Troubleshooting & Optimization Guide"):
    
    trouble_tab1, trouble_tab2, trouble_tab3 = st.tabs(["🎯 Pose Detection Issues", "⚡ Performance Optimization", "📊 MPJPE Understanding"])
    
    with trouble_tab1:
        st.markdown("""
        #### Jika Pose Detection Tidak Akurat:
        
        **🔍 Masalah Deteksi Landmarks:**
        - **Pencahayaan kurang**: Tingkatkan cahaya, hindari bayangan
        - **Background mengganggu**: Gunakan background polos berwarna solid
        - **Pakaian tidak sesuai**: Ganti ke athletic wear yang pas di badan
        - **Jarak tidak optimal**: Posisikan 2-3 meter dari kamera
        - **Sudut kamera salah**: Gunakan side view untuk squat analysis
        
        **🚫 Masalah Joint Occlusion:**
        - **Tubuh terpotong**: Pastikan full body terlihat dengan margin
        - **Self-occlusion**: Hindari pose yang menutupi joint penting
        - **Objek penghalang**: Bersihkan area dari furnitur/obstacles
        - **Multiple person**: Pastikan hanya satu orang dalam frame
        
        **⚙️ Pengaturan Teknis:**
        - **Resolusi rendah**: Gunakan minimal 720p untuk webcam
        - **Frame rate drop**: Tutup aplikasi lain yang berat
        - **Motion blur**: Lakukan gerakan yang controlled dan smooth
        """)
    
    with trouble_tab2:
        st.markdown("""
        #### Optimasi Performa Sistem:
        
        **🖥️ Hardware Requirements:**
        - **CPU**: Intel i5/AMD Ryzen 5 atau lebih tinggi
        - **RAM**: Minimum 8GB, recommended 16GB
        - **Webcam**: 720p atau 1080p dengan good sensor
        - **Internet**: Stable connection untuk live streaming
        
        **🚀 Tips Performa:**
        - **Close unnecessary apps** yang menggunakan camera/CPU
        - **Use tripod/stable mount** untuk mengurangi processing load
        - **Optimal lighting** mengurangi noise dan meningkatkan akurasi
        - **Consistent environment** untuk stable detection
        
        **📱 Browser Optimization:**
        - **Chrome/Edge recommended** untuk WebRTC support
        - **Allow camera permissions** dan microphone access
        - **Disable browser extensions** yang bisa interfere
        - **Clear browser cache** jika ada masalah loading
        """)
    
    with trouble_tab3:
        st.markdown("""
        #### Memahami MPJPE (Mean Per Joint Position Error):
        
        **📏 Interpretasi Nilai MPJPE:**
        - **< 5 pixels**: Akurasi excellent, setup optimal
        - **5-10 pixels**: Akurasi good, suitable untuk analysis
        - **10-15 pixels**: Akurasi fair, masih dapat digunakan
        - **15-25 pixels**: Akurasi poor, perlu perbaikan setup
        - **> 25 pixels**: Akurasi very poor, check semua requirements
        
        **🎯 Faktor yang Mempengaruhi MPJPE:**
        - **Camera angle**: Side view memberikan error lebih rendah
        - **Distance**: 2-3 meter optimal untuk balance detail vs full body
        - **Lighting quality**: Even lighting mengurangi detection errors
        - **Subject movement**: Slow controlled movement lebih akurat
        - **Clothing**: Tight fitting clothes mengurangi landmark ambiguity
        
        **💡 Tips Menurunkan MPJPE:**
        - Gunakan **professional lighting setup** jika memungkinkan
        - **Kalibrasi kamera position** untuk sudut optimal
        - **Warm-up detection** dengan beberapa frame sebelum mulai
        - **Check joint visibility** sebelum memulai recording
        """)
    

st.markdown("""
### ✅ Quick Setup Checklist

Sebelum memulai analisis, pastikan checklist berikut sudah terpenuhi:
""")

checklist_col1, checklist_col2 = st.columns(2)

with checklist_col1:
    st.markdown("""
    **📹 Video Setup:**
    - [ ] Resolusi minimal 720p
    - [ ] Orientasi landscape/horizontal
    - [ ] Kamera stabil (gunakan tripod)
    - [ ] Frame rate 24-30 FPS
    
    **💡 Lighting & Environment:**
    - [ ] Pencahayaan terang dan merata
    - [ ] Background polos dan kontras
    - [ ] Tidak ada bayangan pada tubuh
    - [ ] Area kosong 2x2 meter
    """)

with checklist_col2:
    st.markdown("""
    **👤 Positioning:**
    - [ ] Full body terlihat (kepala-kaki)
    - [ ] Jarak 2-3 meter dari kamera
    - [ ] Posisi side view untuk squat
    - [ ] Semua joint landmarks visible
    
    **👕 Clothing & Preparation:**
    - [ ] Athletic wear yang pas
    - [ ] Warna kontras dengan background
    - [ ] Satu orang dalam frame
    - [ ] Siap untuk gerakan controlled
    """)

st.info("💡 **Pro Tip**: Lakukan test shot pendek (5-10 detik) untuk memverifikasi setup sebelum recording lengkap!")

st.markdown("""
## Quick Navigation
""")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button('📷️ Live Stream', help="Analisis real-time menggunakan webcam"):
        st.switch_page('pages/1_📷️_Live_Stream.py')
with col2:
    if st.button('📂 Upload Video', help="Upload dan analisis video rekaman"):
        st.switch_page('pages/2_ ⬆️_Upload_Video.py')
with col3:
    if st.button('📊 MPJPE Analysis', help="Pelajari metrik evaluasi pose estimation"):
        st.switch_page('pages/3_📊_MPJPE_Analysis.py')

st.markdown("""
---

<sub>Squat Vision is developed using MediaPipe and OpenCV | For best results, follow the setup guidelines above</sub>
""", unsafe_allow_html=True)