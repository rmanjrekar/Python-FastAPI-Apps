# video_converter/routes.py
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from models.users import User
from services.user_service import get_current_user, get_db
from fastapi.security import OAuth2PasswordBearer
from services.vc_service import convert_video_to_mp3

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/convert-to-mp3")
def convert_to_mp3(
    file: UploadFile,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return convert_video_to_mp3(file, user, db)
