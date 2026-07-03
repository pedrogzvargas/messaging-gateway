from modules.shared.aggregate_root.domain import AggregateRoot


class Permission(AggregateRoot):
    """
    Permission entity
    """

    def __init__(self, id, name, is_active, created_at, updated_at):
        super().__init__()
        self.id = id
        self.name = name
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
