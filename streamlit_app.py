import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Tutor Kilat AI",
    page_icon="⚡",
    layout="centered"
)

# --- JUDUL & HEADER ---
st.title("⚡ Tutor Kilat")
st.subheader("Ubah materi buku yang ribet jadi bahasa tongkrongan yang asik!")
st.caption("Hackathon SMK AI Innovator 2025")

# --- SIDEBAR: KONFIGURASI API ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    st.markdown("""
    **Cara Pakai:**
    1. Masukkan API Key Google Gemini (Gratis).
    2. Pilih gaya bahasa tutor kamu.
    3. Foto buku pelajaranmu.
    4. Klik 'Jelaskan!'
    """)

    # Input API Key (Agar aman dan tidak hardcoded)
    api_key = st.text_input("Masukkan Google Gemini API Key", type="password")

    st.divider()
    st.info("Dibuat untuk Hackathon SMK AI Innovator 2025")

# --- FITUR UTAMA: PILIH GAYA BAHASA ---
style_option = st.selectbox(
    "Pilih Gaya Tutor Kamu:",
    ("Anak Tongkrongan (Jaksel/Gaul)", "Gamers Sejati", "Wibu/Anime", "Komedian Stand-up")
)

# Menentukan System Prompt berdasarkan pilihan user
if style_option == "Anak Tongkrongan (Jaksel/Gaul)":
    persona = "Kamu adalah teman tongkrongan anak SMA di Jakarta Selatan. Gunakan istilah seperti 'literally', 'jujurly', 'vibes', 'relate', 'bro/sis'. Jelaskan dengan santai tapi poin utamanya dapat."
elif style_option == "Gamers Sejati":
    persona = "Kamu adalah pro player game. Gunakan analogi game seperti 'HP', 'Mana', 'Buff', 'Nerf', 'Level Up', 'Boss Fight'. Anggap materi pelajaran adalah tutorial game."
elif style_option == "Wibu/Anime":
    persona = "Kamu adalah karakter anime yang semangat (shonen). Gunakan istilah seperti 'Nakama', 'Chakra', 'Kekuatan', dan ekspresi semangat. Anggap materi ini adalah jurus rahasia."
else:
    persona = "Kamu adalah komedian stand-up yang lucu. Jelaskan materi ini dengan punchline yang bikin ketawa tapi tetap edukatif."

# --- INPUT GAMBAR (KAMERA & UPLOAD) ---
st.subheader("📸 Masukkan Materi Pelajaran")
tab1, tab2 = st.tabs(["Ambil Foto", "Upload Gambar"])

image = None

with tab1:
    camera_file = st.camera_input("Jepret halaman buku")
    if camera_file:
        image = Image.open(camera_file)

with tab2:
    upload_file = st.file_uploader("Upload foto buku", type=['jpg', 'png', 'jpeg'])
    if upload_file:
        image = Image.open(upload_file)

# --- PROSES AI ---
if image is not None:
    st.image(image, caption="Materi yang akan dipelajari", use_column_width=True)

    # Tombol Aksi
    if st.button("⚡ Jelaskan Dong, Sepuh!", type="primary"):
        if not api_key:
            st.error("Waduh! API Key belum diisi di menu sebelah kiri (Sidebar).")
        else:
            try:
                with st.spinner('Lagi mikir keras... Tunggu bentar ya!'):
                    # Konfigurasi Gemini
                    genai.configure(api_key=api_key)
                    # Update model ke gemini-2.0-flash-exp sesuai request
                    model = genai.GenerativeModel('gemini-2.0-flash')

                    # Prompt gabungan (Instruksi + Gambar)
                    full_prompt = f"""
                    Peran: {persona}
                    Tugas: Baca teks yang ada di dalam gambar ini. Identifikasi konsep utamanya.
                    Lalu, jelaskan ulang materi tersebut dalam Bahasa Indonesia sesuai peranmu di atas.
                    Buat penjelasannya singkat, padat, dan sangat mudah dimengerti oleh remaja SMK.
                    Format: Berikan judul yang menarik, lalu isi penjelasan, dan akhiri dengan 'Kesimpulan Satu Kalimat'.
                    """

                    # Request ke AI
                    response = model.generate_content([full_prompt, image])

                    # Tampilkan Hasil
                    st.success("Nah, gini maksudnya:")
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
                        {response.text}
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Yah error bro: {e}")

else:
    st.info("👈 Silakan ambil foto atau upload gambar dulu ya.")