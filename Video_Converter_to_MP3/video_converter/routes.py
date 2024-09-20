# video_converter/routes.py
import os
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from users.routes import User, get_current_user, get_db
from fastapi.security import OAuth2PasswordBearer
from fastapi import status
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from tempfile import TemporaryDirectory
from fastapi.responses import FileResponse
from starlette.requests import Request
import pydub

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

TEMP_DIR_NAME = "temp_files"  # Name of the subfolder
TEMP_DIR_PATH = os.path.join(os.path.dirname(__file__), TEMP_DIR_NAME)
os.makedirs(TEMP_DIR_PATH, exist_ok=True)

# Set the path to the ffmpeg executable
ffmpeg_path = "C:\\Users\\rohit manjrekar\\scoop\\apps\\ffmpeg\\6.0\\bin\\ffmpeg.exe" 
pydub.AudioSegment.converter = ffmpeg_path

def convert_video_to_mp3(file: UploadFile, user: User, db: Session) -> FileResponse:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    
    video_path = os.path.join(TEMP_DIR_PATH, file.filename)
    with open(video_path, "wb") as f:
        f.write(file.file.read())

    filename_wo_extension = os.path.splitext(file.filename)[0]

    # Convert the video to audio using moviepy and save as MP3
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    mp3_audio_path = os.path.join(TEMP_DIR_PATH, f"{filename_wo_extension}.mp3")
    audio_clip.write_audiofile(mp3_audio_path, codec="mp3")

    return FileResponse(mp3_audio_path, media_type="audio/mpeg")

@router.post("/convert-to-mp3")
def convert_to_mp3(
    file: UploadFile,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return convert_video_to_mp3(file, user, db)
