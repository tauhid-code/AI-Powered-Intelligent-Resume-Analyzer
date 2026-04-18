"""
  POST /auth/signup  → create account
  POST /auth/login   → return JWT
  GET  /auth/me      → return profile (protected)
"""

from fastapi import APIRouter, Depends, HTTPException, status 
from backend.database import get_db 
from backend.dependencies import get_current_user 
from backend.models import LoginRequest, MessageResponse, SignupRequest, TokenResponse, UserPublic
from backend.utils.security import create_access_token, hash_password, verify_password

router = APIRouter() 

## 1. POST/auth/signup 
@router.post("/signup", response_model = MessageResponse, status_code = status.HTTP_201_CREATED)

def signup(payload: SignupRequest):
    with get_db() as conn: 
        existing =conn.execute(
            "SELECT id FROM users WHERE email = ?",(payload.email,)
        ).fetchone()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )
        conn.execute(
            "INSERT INTO users(name, email, password) VALUES(?,?,?)",
            (payload.name.strip(), payload.email.lower(), hash_password(payload.password)),
        )
        return {"message": "Account created successfully. Please log in"}

## 2. POST/auth/login

@router.post("/login", response_model = TokenResponse)

def login(payload: LoginRequest): 
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, name, email, password FROM users where email = ?", 
            (payload.email.lower(),),
        ).fetchone()

        if row is None or not verify_password(payload.password, row["password"]):
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail ="Incorrect email or password.",
            )
        token = create_access_token(
        data={"sub": row["email"], "name": row["name"], "id": row["id"]}
    )
    
    return TokenResponse(
        access_token=token,
        name = row["name"],
        email = row["email"],
    )
