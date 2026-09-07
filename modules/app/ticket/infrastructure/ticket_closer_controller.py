from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.ticket.domain import TicketRepository
from modules.app.ticket.domain.exceptions import TicketDoesNotExist
from modules.app.ticket.application import TicketCloser
from modules.app.ticket.infrastructure import PgTicketRepository
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.logger.domain import Logger
from modules.shared.logger.infrastructure import PyLogger
from .ticket_response import TicketResponse


class TicketCloserController:
    """
    Class controller to close a Ticket owned by the current user
    """

    def __init__(
        self,
        session: AsyncSession,
        unit_of_work: UnitOfWork | None = None,
        ticket_repository: TicketRepository | None = None,
        environ: Environ | None = None,
        logger: Logger | None = None,
    ):
        """
        Args:
            session: database session
            unit_of_work: unit of work
            ticket_repository: repository for ticket database table operations
            environ: environ variable reader
            logger: logger
        """

        self.__session = session
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__ticket_repository = ticket_repository or PgTicketRepository(session=self.__session)
        self.__environ = environ or PyEnviron()
        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    async def close(self, ticket_id: UUID, user_id: UUID):
        try:
            ticket_closer = TicketCloser(
                unit_of_work=self.__unit_of_work,
                ticket_repository=self.__ticket_repository,
            )
            ticket = await ticket_closer.close(ticket_id=ticket_id, user_id=user_id)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": TicketResponse.model_validate(ticket),
            }, status.HTTP_200_OK

        except TicketDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            self.__logger.error(f"TicketCloserController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
