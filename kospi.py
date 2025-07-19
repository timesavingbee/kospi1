import os
import urllib.request
import stat

FFMPEG_DIR = "ffmpeg"
FFMPEG_BIN = os.path.join(FFMPEG_DIR, "ffmpeg")
FFPROBE_BIN = os.path.join(FFMPEG_DIR, "ffprobe")

def setup_ffmpeg():
    if not os.path.exists(FFMPEG_DIR):
        os.makedirs(FFMPEG_DIR)

    if not os.path.exists(FFMPEG_BIN):
        print("🔽 ffmpeg 다운로드 중...")
        urllib.request.urlretrieve(
            "https://www.johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz",
            "ffmpeg.tar.xz"
        )

        import tarfile
        with tarfile.open("ffmpeg.tar.xz") as tar:
            members = [m for m in tar.getmembers() if "ffmpeg" in m.name or "ffprobe" in m.name]
            for member in members:
                name = os.path.basename(member.name)
                tar.extract(member, FFMPEG_DIR)
                os.rename(os.path.join(FFMPEG_DIR, member.name), os.path.join(FFMPEG_DIR, name))

        os.chmod(FFMPEG_BIN, stat.S_IRWXU)
        os.chmod(FFPROBE_BIN, stat.S_IRWXU)
        print("✅ ffmpeg 설치 완료")

# 설치 실행
setup_ffmpeg()
