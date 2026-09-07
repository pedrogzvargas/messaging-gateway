from uuid import UUID


class Customer:

    PATCHABLE_FIELDS = {"name", "last_name", "second_last_name"}

    def __init__(self, id: UUID, name: str, last_name: str, second_last_name:str):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.second_last_name = second_last_name

    def patch(self, data: dict):
        for attr, value in data.items():
            if attr in self.PATCHABLE_FIELDS:
                setattr(self, attr, value)
