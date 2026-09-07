from pydantic import BaseModel
from pydantic import EmailStr


class Login(BaseModel):
    email: EmailStr
    password: str


class LoginResponseBody(BaseModel):
    access_token: str
    refresh_token: str


class LoginResponse(BaseModel):
    success: bool
    message: str
    data: LoginResponseBody


class RetryAfterData(BaseModel):
    retry_after: int


class TooManyLoginAttemptsResponse(BaseModel):
    success: bool
    message: str
    data: RetryAfterData


class RefreshToken(BaseModel):
    refresh_token: str


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    password: str


class ChangePassword(BaseModel):
    password: str
    new_password: str
