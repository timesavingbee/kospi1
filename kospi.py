import streamlit as st
import yt_dlp
import os
import uuid

st.set_page_config(page_title="YouTube to MP3", page_icon="🎧")
st.title("🎵 유튜브 → MP3 변환기")

url = st.text_input("유튜브 URL 입력")

if st.button("MP3 다운로드") and url:
    try:
        temp_id = str(uuid.uuid4())
        filename_template = f"{temp_id}.%(ext)s"

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': filename_template,
            'ffmpeg_location': './ffmpeg',  # 로컬 폴더 경로
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "youtube_audio")
            mp3_path = f"{temp_id}.mp3"

        with open(mp3_path, "rb") as f:
            st.success(f"✅ {title} MP3 다운로드 준비 완료!")
            st.download_button("📥 MP3 다운로드", f, file_name=f"{title}.mp3", mime="audio/mpeg")

        os.remove(mp3_path)

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
