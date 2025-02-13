from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    role = fields.Str(dump_only=True)


class UserOptionalSchema(Schema):
    id = fields.Int(required=False)


class UserAddSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    role = fields.Str(required=True)


class UserDeleteSchema(Schema):
    email = fields.Str(required=True)
