from environs import Env
from pathlib import Path
from modules.shared.environ.domain import Environ


class PyEnviron(Environ):
    """
    Python Environ Implementation
    """

    def __init__(self, env_file_path=None):
        """
        PyEnviron constructor
        :param env_file_path:
        """

        self.__environ = Env()
        env_file_path = env_file_path or str(
            Path(__file__).resolve(strict=True).parent.parent.parent.parent.parent / '.env')
        self.__environ.read_env(path=env_file_path)

    def get_str(self, key, default=None):
        return self.__environ.str(key, default)

    def get_int(self, key, default=None):
        return self.__environ.int(key, default)

    def get_bool(self, key, default=None):
        return self.__environ.bool(key, default)
