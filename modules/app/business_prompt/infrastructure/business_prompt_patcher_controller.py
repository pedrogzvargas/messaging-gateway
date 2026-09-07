from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.business_prompt.domain import BusinessPromptRepository
from modules.app.business_prompt.domain.exceptions import BusinessDoesNotExist
from modules.app.business_prompt.domain.exceptions import BusinessPromptDoesNotExist
from modules.app.business_prompt.application import BusinessPromptPatcher
from modules.app.business_prompt.infrastructure import PgBusinessPromptRepository
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.shared.http.domain import status
from modules.shared.http.domain import messages


class BusinessPromptPatcherController:
    """
    Class controller to patch a single Business Prompt of a user's business, by key
    """

    def __init__(
        self,
        session: AsyncSession,
        unit_of_work: UnitOfWork | None = None,
        business_prompt_repository: BusinessPromptRepository | None = None,
    ):
        """
        Args:
            session: database session
            unit_of_work: unit of work to persist the change
            business_prompt_repository: repository for business prompt database table operations
        """

        self.__session = session
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__business_prompt_repository = business_prompt_repository or PgBusinessPromptRepository(session=self.__session)

    async def patch(self, user_id: UUID, key: str, data: dict):
        try:
            business_prompt_patcher = BusinessPromptPatcher(
                unit_of_work=self.__unit_of_work,
                business_prompt_repository=self.__business_prompt_repository,
            )
            await business_prompt_patcher.patch(user_id=user_id, key=key, data=data)

            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
            }, status.HTTP_200_OK

        except BusinessDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}"}, status.HTTP_404_NOT_FOUND
            return response

        except BusinessPromptDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}"}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
