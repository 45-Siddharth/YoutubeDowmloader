from fastapi import FastAPI, HTTPException, Form
import yt_dlp
import os
import tempfile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Configure CORS to allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider restricting to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/download")
def download_videos_from_channel(link: str = Form(...), num_videos: int = Form(...)):
    try:
        # Use a temporary directory for storing the downloaded videos
        temp_dir = tempfile.gettempdir()

        # Ensure the output template is compatible with mobile file systems
        output_template = os.path.join(temp_dir, '/storage/emulated/0/Download/%(title)s.%(ext)s')

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4a]/best',
            'outtmpl': output_template,
            'noplaylist': True,
            'playlistend': num_videos,
            'quiet': False,
        }

        # Download the videos
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        return JSONResponse(content={"status": "Download started", "output_dir": temp_dir})

    except yt_dlp.utils.DownloadError as e:
        # Handle yt-dlp specific errors
        return JSONResponse(
            status_code=400,
            content={"error": "Download failed", "details": str(e)}
        )
    except Exception as e:
        # Handle general errors
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# from fastapi import FastAPI, HTTPException, Form
# import yt_dlp
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = ["*"],
#     allow_credentials = True,
#     allow_methods = ["*"],
#     allow_headers = ["*"],
# )

# @app.post("/download")
# def download_videos_from_channel(link: str = Form(...), num_videos: int = Form(...)):
#     ydl_opts = {
#         'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4a]/best',
#         'outtmpl': '/storage/emulated/0/Download/%(title)s.%(ext)s',
#         'noplaylist': True,
#         'playlistend': num_videos,
#         'quiet': False,
#     }
#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([link])
#         return {"status": "Download started"}
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


