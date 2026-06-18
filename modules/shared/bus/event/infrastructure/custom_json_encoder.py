from uuid import UUID
from datetime import datetime
from decimal import Decimal
import json


class CustomJSONEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, UUID):
            return str(obj)

        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, Decimal):
            return float(obj)

        if isinstance(obj, set):
            return list(obj)

        return super().default(obj)
