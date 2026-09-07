from uuid import UUID
from fastapi import APIRouter
from fastapi import Response
from fastapi import Depends
from modules.shared.http.domain import status
from modules.shared.http.infrastructure import ErrorResponse
from modules.shared.http.infrastructure import SuccessResponse
from modules.shared.auth.infrastructure.controllers import LoginController
from modules.shared.auth.infrastructure.controllers import LogoutController
from modules.shared.auth.infrastructure.controllers import RefreshTokenController
from modules.shared.auth.infrastructure.controllers import PasswordRecoveryController
from modules.shared.auth.infrastructure.controllers import PasswordResetController
from modules.shared.auth.infrastructure.controllers import PasswordChangeController
from fast_app.api.v1.shared.scehmas.auth import Login
from fast_app.api.v1.shared.scehmas.auth import LoginResponse
from fast_app.api.v1.shared.scehmas.auth import TooManyLoginAttemptsResponse
from fast_app.api.v1.shared.scehmas.auth import RefreshToken
from fast_app.api.v1.shared.scehmas.auth import ForgotPassword
from fast_app.api.v1.shared.scehmas.auth import ResetPassword
from fast_app.api.v1.shared.scehmas.auth import ChangePassword
from fast_app.core.db_session import get_session
from fast_app.core.auth import get_current_user

router = APIRouter()

@router.post(
    "/login",
    response_model=LoginResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": TooManyLoginAttemptsResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
async def login(payload: Login, db_session = Depends(get_session)):
    login_controller = LoginController(session=db_session)
    controller_response = await login_controller.login(body=payload.model_dump())
    return controller_response

@router.post(
    "/logout",
    response_model=SuccessResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
async def logout(response: Response, db_session = Depends(get_session), current_user = Depends(get_current_user)):
    logout_controller = LogoutController(session=db_session)
    controller_response, code = await logout_controller.logout(jti=UUID(current_user.get("jti")))
    response.status_code = code
    return controller_response

@router.post(
    "/refresh-token",
    response_model=LoginResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
async def refresh_token(response: Response, payload: RefreshToken, db_session = Depends(get_session)):
    refresh_token_controller = RefreshTokenController(session=db_session)
    controller_response, code = await refresh_token_controller.refresh(body=payload.model_dump())
    response.status_code = code
    return controller_response

@router.post(
    "/forgot-password",
    response_model=SuccessResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
async def forgot_password(response: Response, payload: ForgotPassword, db_session = Depends(get_session)):
    password_recovery_controller = PasswordRecoveryController(session=db_session)
    controller_response, code = await password_recovery_controller.recover(body=payload.model_dump())
    response.status_code = code
    return controller_response

@router.post(
    "/reset-password",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
async def reset_password(response: Response, payload: ResetPassword, db_session = Depends(get_session)):
    password_reset_controller = PasswordResetController(session=db_session)
    controller_response, code = await password_reset_controller.reset(body=payload.model_dump())
    response.status_code = code
    return controller_response

@router.post(
    "/change-password",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
async def reset_password(
        response: Response,
        payload: ChangePassword,
        db_session = Depends(get_session),
        current_user = Depends(get_current_user)
):
    password_change_controller = PasswordChangeController(session=db_session)
    controller_response, code = await password_change_controller.change(
        user_id=UUID(current_user.get("sub")),
        body=payload.model_dump()
    )
    response.status_code = code
    return controller_response
