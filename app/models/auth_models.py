from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str
    phone_number: str
    gender: str  # "MALE" | "FEMALE" | "OTHER"
    role: str = "Admin"  # default role


class RegisterResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
