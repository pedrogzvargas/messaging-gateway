from modules.shared.aggregate_root.domain import AggregateRoot


class RefreshToken(AggregateRoot):
    """
    RefreshToken entity
    """

    def __init__(self, id, user_id, jti, revoked, created_at, updated_at):
        super().__init__()
        self.id = id
        self.user_id = user_id
        self.jti = jti
        self.revoked = revoked
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(id, user_id, jti, revoked=False, created_at=None, updated_at=None):
        return RefreshToken(
            id=id,
            user_id=user_id,
            jti=jti,
            revoked=revoked,
            created_at=created_at,
            updated_at=updated_at,
        )

    def patch(self, data: dict):
        for attr, value in data.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

    def to_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            jti=self.jti,
            revoked=self.revoked,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
