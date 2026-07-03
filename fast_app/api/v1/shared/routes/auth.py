from fastapi import APIRouter
from fastapi import Response
from fastapi import Depends
from modules.shared.auth.infrastructure.controllers import LoginController
from modules.shared.auth.infrastructure.controllers import LogoutController
from modules.shared.auth.infrastructure.controllers import RefreshTokenController
from modules.shared.auth.infrastructure.controllers import PasswordRecoveryController
from modules.shared.auth.infrastructure.controllers import PasswordResetController
from fast_app.api.v1.shared.scehmas.auth import Login
from fast_app.api.v1.shared.scehmas.auth import Logout
from fast_app.api.v1.shared.scehmas.auth import RefreshToken
from fast_app.api.v1.shared.scehmas.auth import ForgotPassword
from fast_app.api.v1.shared.scehmas.auth import ResetPassword
from fast_app.core.db_session import get_session
from fast_app.core.auth import get_current_user

router = APIRouter()

@router.post("/login")
async def login(response: Response, payload: Login, db_session = Depends(get_session)):
    login_controller = LoginController(session=db_session)
    controller_response, code = await login_controller.login(body=payload.model_dump())
    response.status_code = code
    return controller_response

@router.post("/logout")
async def logout(response: Response, payload: Logout, db_session = Depends(get_session), _ = Depends(get_current_user)):
    logout_controller = LogoutController(session=db_session)
    controller_response, code = await logout_controller.logout(body=payload.model_dump())
    response.status_code = code
    return controller_response

@router.post("/refresh-token")
async def refresh_token(response: Response, payload: RefreshToken, db_session = Depends(get_session)):
    refresh_token_controller = RefreshTokenController(session=db_session)
    controller_response, code = await refresh_token_controller.refresh(body=payload.model_dump())
    response.status_code = code
    return controller_response

@router.post("/forgot-password")
async def forgot_password(response: Response, payload: ForgotPassword, db_session = Depends(get_session)):
    password_recovery_controller = PasswordRecoveryController(session=db_session)
    controller_response, code = await password_recovery_controller.recover(body=payload.model_dump())
    response.status_code = code
    return controller_response

@router.post("/reset-password")
async def reset_password(response: Response, payload: ResetPassword, db_session = Depends(get_session)):
    password_reset_controller = PasswordResetController(session=db_session)
    controller_response, code = await password_reset_controller.recover(body=payload.model_dump())
    response.status_code = code
    return controller_response
