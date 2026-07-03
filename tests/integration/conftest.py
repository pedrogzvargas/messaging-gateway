from sqlalchemy.dialects import postgresql
from sqlalchemy.types import TypeDecorator, TEXT
import json

class SQLiteJSON(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        return json.dumps(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return json.loads(value) if value is not None else None

import sqlalchemy
if sqlalchemy.engine.url.make_url("sqlite:///").get_backend_name() == 'sqlite':
    postgresql.JSONB = SQLiteJSON
