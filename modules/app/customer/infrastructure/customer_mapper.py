from sqlalchemy_models import CustomerModel
from modules.app.customer.domain import Customer


class CustomerMapper:

    @staticmethod
    def to_domain(model: CustomerModel) -> Customer:
        return Customer(
            id=model.id,
            name=model.name,
            last_name=model.last_name,
            second_last_name=model.second_last_name,
        )
