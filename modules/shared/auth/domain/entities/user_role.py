from modules.shared.aggregate_root.domain import AggregateRoot


class UserRole(AggregateRoot):
    """
    User entity
    """

    def __init__(self, id, user_id, role_id, is_active, created_at, updated_at):
        super().__init__()
        self.id = id
        self.user_id = user_id
        self.role_id = role_id
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            role_id=self.role_id,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
