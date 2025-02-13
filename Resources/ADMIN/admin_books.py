from Library_Backend_Api.Data_Base.book_data_base import LibraryBooksDataBase
from Library_Backend_Api.Schemas.Books_Schema import BooksSchema, BooksGetSchema, BooksAddSchema, BooksUpdateSchema
from Library_Backend_Api.id_generator import generate_id
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from flask import request,jsonify
import cloudinary.uploader

blp = Blueprint('books', __name__, description='operation on books....')


@blp.route("/admin_books")
class Books(MethodView):
	def __init__(self):
		self.books_database = LibraryBooksDataBase()

	@jwt_required()
	@blp.response(200, BooksSchema(many=True))
	@blp.arguments(BooksGetSchema, location='query')
	def get(self, args):
		book_name = args.get('BooksTitle')
		if book_name is None:
			return jsonify(self.books_database.get_books())
		else:
			result = self.books_database.books_get_through_name(book_name)
			if result is None:
				abort(404, message="record not found....")
			return result


@blp.route("/add-book")
class AddBook(MethodView):
	def __init__(self):
		self.book = LibraryBooksDataBase()

	@jwt_required()
	def post(self):
		try:
			book_data = {
				"BooksTitle": request.form.get("BooksTitle"),
				"author": request.form.get("author"),
				"genre": request.form.get("genre"),
				"published_date": request.form.get("published_date"),
				"available_copies": request.form.get("available_copies")
			}
			image_file = request.files.get("image")

			if image_file:
				upload_result = cloudinary.uploader.upload(image_file)
				image_url = upload_result["secure_url"]
			else:
				image_url = None
			book_id = generate_id()
			response = self.book.add_books(book_id, book_data, image_url)
			return response, 201
		except Exception as e:
			return {"error": str(e)}, 500


# @blp.route("/add-book")
# class AddBook(MethodView):
# 	def __init__(self):
# 		self.book = LibraryBooksDataBase()
#
# 	@jwt_required()
# 	def post(self):
# 		request_data = request.get_json()
# 		self.book.add_books(generate_id(), request_data)
# 		return {"message": 'books added successfully....'}


@blp.route("/admin-update-book")
class AdminUpdateBook(MethodView):
	def __init__(self):
		self.book_data = LibraryBooksDataBase()

	@jwt_required()
	def put(self):
		request_data = request.get_json()

		self.book_data.update_books(request_data['available_copies'], request_data['BooksTitle'])
		return {"message": "update successfully...."}


@blp.route("/admin-book-delete")
class AdminBookDelete(MethodView):
	def __init__(self):
		self.book_data = LibraryBooksDataBase()

	@jwt_required()
	def delete(self):
		request_data = request.args.get("BooksTitle")
		print(request_data)
		if self.book_data.delete_books(request_data):
			return {"message": "deleted successfully..."}
		abort(404, message="record not found...")
