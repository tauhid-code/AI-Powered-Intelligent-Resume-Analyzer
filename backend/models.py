## Pydantic requests and response models for Hirelytics AI FastAPI backend.

from pydantic import BaseModel, EmailStr, Field 

##---Request models---
class SignupRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length =100, example = "Tauhid Ur Rehman") 
    email: EmailStr = Field(..., example = "tauhid@example.com")
    password: str = Field(..., min_length=8, example = "strongpass123")


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="tauhid@example.com")
    password: str = Field(..., min_length=1, example="strongpass123")


##---Response models---
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    name: str
    email: str


class MessageResponse(BaseModel):
    message: str


class UserPublic(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
