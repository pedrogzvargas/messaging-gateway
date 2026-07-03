from pydantic import BaseModel
from pydantic import EmailStr


class Login(BaseModel):
    email: EmailStr
    password: str


class RefreshToken(BaseModel):
    refresh_token: str


class Logout(BaseModel):
    refresh_token: str


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    password: str
