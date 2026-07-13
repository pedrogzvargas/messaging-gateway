from sqlalchemy_models import ContactModel
from modules.app.contact.domain import Contact


class ContactMapper:

    @staticmethod
    def to_model(entity: Contact) -> ContactModel:
        return ContactModel(
            id=entity.id,
            channel_account_id=entity.channel_account_id,
            provider_id=entity.provider_id,
            display_name=entity.display_name,
        )

    @staticmethod
    def to_domain(model: ContactModel) -> Contact:
        return Contact(
            id=model.id,
            channel_account_id=model.channel_account_id,
            provider_id=model.provider_id,
            display_name=model.display_name,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
