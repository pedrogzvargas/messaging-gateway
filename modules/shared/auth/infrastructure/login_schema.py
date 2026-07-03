from marshmallow import Schema, fields


class LoginSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()
