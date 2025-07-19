# streamlit_app.py

import streamlit as st
import yt_dlp
import os
import uuid

st.set_page_config(page_title="YouTube to MP3", page_icon="🎧")

st.title("🎵 YouTube → MP3 변환기")
url = st.text_input("유튜브 영상 URL을 입력하세요:")

if st.button("MP3 다운로드"):
    if not url:
        st.warning("URL을 입력해주세요.")
    else:
        try:
            st.info("MP3로 변환 중입니다. 잠시만 기다려주세요...")

            # 임시 저장 파일명
            temp_id = str(uuid.uuid4())
            output_filename = f"{temp_id}.%(ext)s"

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_filename,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "youtube_audio")
                filename = f"{temp_id}.mp3"

            with open(filename, "rb") as f:
                st.success(f"✅ {title} 다운로드 준비 완료!")
                st.download_button(
                    label="📥 MP3 파일 다운로드",
                    data=f,
                    file_name=f"{title}.mp3",
                    mime="audio/mpeg"
                )

            os.remove(filename)

        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")
