from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.customer.domain import CustomerRepository
from modules.app.customer.domain.exceptions import CustomerDoesNotExist
from modules.app.customer.infrastructure import PgCustomerRepository
from modules.app.customer.application import CustomerFinder
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.logger.domain import Logger
from modules.shared.logger.infrastructure import PyLogger
from .customer_response import CustomerResponse


class CustomerFinderController:
    """
    Class controller to get Customer
    """

    def __init__(
        self,
        session: AsyncSession,
        customer_repository: CustomerRepository | None = None,
        environ: Environ | None = None,
        logger: Logger | None = None,
    ):
        """
        Args:
            session: database session
            customer_repository: repository for customer database table operations
            environ: environ variable reader
            logger: logger
        """

        self.__session = session
        self.__customer_repository = customer_repository or PgCustomerRepository(session=self.__session)
        self.__environ = environ or PyEnviron()
        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    async def find(self, customer_id: UUID):
        try:
            customer_finder = CustomerFinder(customer_repository=self.__customer_repository)
            customer = await customer_finder.find(customer_id=customer_id)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": CustomerResponse.model_validate(customer),
            }, status.HTTP_200_OK

        except CustomerDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}"}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            self.__logger.error(f"CustomerFinderController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
