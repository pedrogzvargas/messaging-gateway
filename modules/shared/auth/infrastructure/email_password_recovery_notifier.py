from email.mime.text import MIMEText
import smtplib
from modules.shared.auth.domain import PasswordRecoveryNotifier
from modules.shared.auth.domain.entities import User
from modules.shared.environ.domain import Environ


class EmailPasswordRecoveryNotifier(PasswordRecoveryNotifier):

    def __init__(self, email_client, environ: Environ):
        self.__email_client = email_client
        self.__environ = environ

    def send_reset_link(self, user: User, token: str) -> None:
        link = f"{self.__environ.get_str('FRONTEND_URL')}/reset-password?token={token}"
        email_user = self.__environ.get_str('EMAIL_USER')
        email_pass = self.__environ.get_str('EMAIL_PASS')

        subject = "Recuperación de contraseña"

        body = f"""
            Hola,

            Haz clic aquí:

            {link}

            Este enlace expira en 15 minutos.
        """

        msg = MIMEText(body, "html")
        msg["From"] = email_user
        msg["To"] = user.email
        msg["Subject"] = subject

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.sendmail(email_user, [user.email], msg.as_string())
