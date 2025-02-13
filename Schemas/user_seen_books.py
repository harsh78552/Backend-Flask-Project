from marshmallow import Schema, fields


class UserBookSeen(Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)


class UserBookSeenByTitle(Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    BooksTitle = fields.Str(required=False)
