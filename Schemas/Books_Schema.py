from marshmallow import Schema, fields


class BooksSchema(Schema):
    id = fields.Str(dump_only=True)
    BooksTitle = fields.Str(dump_only=True)
    author = fields.Str(dump_only=True)
    genre = fields.Str(dump_only=True)
    published_date = fields.Str(dump_only=True)
    available_copies = fields.Str(dump_Only=True)


class BooksGetSchema(Schema):
    BooksTitle = fields.Str(required=False)


class BooksAddSchema(Schema):
    BooksTitle = fields.Str(required=True)
    author = fields.Str(required=True)
    genre = fields.Str(required=True)
    published_date = fields.Str(required=True)
    available_copies = fields.Int(required=True)


class BooksUpdateSchema(Schema):
    available_copies = fields.Int(required=True)
    books_title = fields.Str(required=True)


class BooksDeleteSchema(Schema):
    BooksTitle = fields.Str(required=True)
