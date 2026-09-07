from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.customer.domain import CustomerRepository
from modules.app.customer.domain.exceptions import CustomerDoesNotExist
from modules.app.customer.infrastructure import PgCustomerRepository
from modules.app.customer.application import CustomerPatcher
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.logger.domain import Logger
from modules.shared.logger.infrastructure import PyLogger
from .customer_response import CustomerResponse


class CustomerPatcherController:
    """
    Class controller to patch Customer
    """

    def __init__(
        self,
        session: AsyncSession,
        unit_of_work: UnitOfWork | None = None,
        customer_repository: CustomerRepository | None = None,
        environ: Environ | None = None,
        logger: Logger | None = None,
    ):
        """
        Args:
            session: database session
            unit_of_work: unit of work
            customer_repository: repository for customer database table operations
            environ: environ variable reader
            logger: logger
        """

        self.__session = session
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__customer_repository = customer_repository or PgCustomerRepository(session=self.__session)
        self.__environ = environ or PyEnviron()
        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    async def patch(self, customer_id: UUID, data: dict):
        try:
            customer_patcher = CustomerPatcher(
                unit_of_work=self.__unit_of_work,
                customer_repository=self.__customer_repository,
            )
            customer = await customer_patcher.patch(customer_id=customer_id, data=data)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": CustomerResponse.model_validate(customer),
            }, status.HTTP_200_OK

        except CustomerDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}"}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            self.__logger.error(f"CustomerPatcherController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
