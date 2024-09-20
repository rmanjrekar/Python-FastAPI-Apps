from fastapi import FastAPI
from users.routes import router as user_router
from video_converter.routes import router as converter_router

app = FastAPI()

app.include_router(user_router, prefix="", tags=["users"])
app.include_router(converter_router, prefix="/converter", tags=["converter"])
