from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
