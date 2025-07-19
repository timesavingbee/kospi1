import streamlit as st
import yt_dlp
import os
import uuid
import urllib.request
import stat
import tarfile

# ffmpeg 자동 설치 함수
FFMPEG_DIR = "ffmpeg"
FFMPEG_BIN = os.path.join(FFMPEG_DIR, "ffmpeg")
FFPROBE_BIN = os.path.join(FFMPEG_DIR, "ffprobe")

def setup_ffmpeg():
    if not os.path.exists(FFMPEG_BIN) or not os.path.exists(FFPROBE_BIN):
        st.info("🔽 ffmpeg 설치 중입니다. 잠시만 기다려주세요...")
        urllib.request.urlretrieve(
            "https://www.johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz",
            "ffmpeg.tar.xz"
        )
        with tarfile.open("ffmpeg.tar.xz") as tar:
            members = [m for m in tar.getmembers() if os.path.basename(m.name) in ["ffmpeg", "ffprobe"]]
            for member in members:
                name = os.path.basename(member.name)
                tar.extract(member, FFMPEG_DIR)
                os.rename(os.path.join(FFMPEG_DIR, member.name), os.path.join(FFMPEG_DIR, name))
        os.chmod(FFMPEG_BIN, stat.S_IRWXU)
        os.chmod(FFPROBE_BIN, stat.S_IRWXU)
        os.remove("ffmpeg.tar.xz")
        st.success("✅ ffmpeg 설치 완료!")

setup_ffmpeg()

# Streamlit 앱 본문
st.set_page_config(page_title="YouTube to MP3", page_icon="🎧")
st.title("🎵 유튜브 → MP3 변환기")
st.markdown(
    '<h3 style="color:#1f77b4;">잘생긴 아들 Ryan을 위해 만든 완전 공짜 앱입니다.</h3>',
    unsafe_allow_html=True
)

url = st.text_input("유튜브 URL 주소를 입력하고 MP3 다운로드 버튼을 누르시라!")

if st.button("MP3 다운로드") and url:
    try:
        temp_id = str(uuid.uuid4())
        filename_template = f"{temp_id}.%(ext)s"

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': filename_template,
            'ffmpeg_location': FFMPEG_DIR,
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
