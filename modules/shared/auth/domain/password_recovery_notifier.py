from abc import ABC
from abc import abstractmethod
from modules.shared.auth.domain.entities import User


class PasswordRecoveryNotifier(ABC):

    @abstractmethod
    def send_reset_link(self, user: User, token: str) -> None:
        pass
