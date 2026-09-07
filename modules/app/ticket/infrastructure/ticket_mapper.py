from sqlalchemy_models import TicketModel
from modules.app.ticket.domain import Ticket


class TicketMapper:

    @staticmethod
    def to_model(entity: Ticket) -> TicketModel:
        # TicketModel's dataclass fields don't include customer_id (mapped imperatively
        # on the table only), so it has to be set as an attribute after construction.
        model = TicketModel(
            id=entity.id,
            details=entity.details,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
        model.customer_id = entity.customer_id
        return model

    @staticmethod
    def to_domain(model: TicketModel) -> Ticket:
        return Ticket(
            id=model.id,
            customer_id=model.customer_id,
            details=model.details,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
