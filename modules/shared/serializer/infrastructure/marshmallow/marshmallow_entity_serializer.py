from modules.shared.serializer.domain import EntitySerializer


class MarshmallowEntitySerializer(EntitySerializer):
    """
    MarshmallowEntitySerializer
    """

    def __init__(self, schema):
        self.__schema = schema

    def __call__(self, entity, many=False):
        return self.dump(entity, many=many)

    def dump(self, entity, many=False):
        """function to serialize entity"""
        return self.__schema.dump(entity, many=many)
