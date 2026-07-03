from modules.shared.aggregate_root.domain import AggregateRoot


class User(AggregateRoot):
    """
    User entity
    """

    def __init__(self, id, email, username, password, is_active, created_at, updated_at):
        super().__init__()
        self.id = id
        self.email = email
        self.username = username
        self.password = password
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return dict(
            id=self.id,
            email=self.email,
            username=self.username,
            password=self.password,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
