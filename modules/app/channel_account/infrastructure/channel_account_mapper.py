from sqlalchemy_models import ChannelAccountModel
from modules.app.channel_account.domain import ChannelAccount


class ChannelAccountMapper:

    @staticmethod
    def to_model(entity: ChannelAccount) -> ChannelAccountModel:
        return ChannelAccountModel(
            id=entity.id,
            channel_id=entity.channel_id,
            business_id=entity.business_id,
            provider_id=entity.provider_id,
            display_name=entity.display_name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_domain(model: ChannelAccountModel) -> ChannelAccount:
        return ChannelAccount(
            id=model.id,
            channel_id=model.channel_id,
            business_id=model.business_id,
            provider_id=model.provider_id,
            display_name=model.display_name,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
