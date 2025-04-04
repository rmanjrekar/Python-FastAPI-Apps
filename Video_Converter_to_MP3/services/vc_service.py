import os
from schemas.coverter import ConversionResponse
from fastapi import HTTPException, status, UploadFile
from moviepy.editor import VideoFileClip
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from models.users import User

TEMP_DIR_NAME = "temp_files"  # Name of the subfolder
current_dir = os.getcwd()
root_dir = os.path.dirname(current_dir)

TEMP_DIR_PATH = os.path.join(root_dir, TEMP_DIR_NAME)
os.makedirs(TEMP_DIR_PATH, exist_ok=True)

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

    # Return metadata along with file
    response = ConversionResponse(
        filename=f"{filename_wo_extension}.mp3",
        converted_to="mp3",
        message="Video successfully converted to MP3"
    )

    return FileResponse(mp3_audio_path, media_type="audio/mpeg", headers={"X-Conversion-Details": response.model_dump_json()})