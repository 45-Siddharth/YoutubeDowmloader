from fastapi import FastAPI, HTTPException, Form
import yt_dlp
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.post("/download")
def download_videos_from_channel(link: str = Form(...), num_videos: int = Form(...)):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4a]/best',
        'outtmpl': '/storage/emulated/0/Download/%(title)s.%(ext)s',
        'noplaylist': True,
        'playlistend': num_videos,
        'quiet': False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return {"status": "Download started"}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


