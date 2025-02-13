from Library_Backend_Api.Data_Base.user_data_base import LibraryUserDataBase
from Library_Backend_Api.Data_Base.book_data_base import LibraryBooksDataBase
from Library_Backend_Api.Schemas.user_seen_books import UserBookSeen, UserBookSeenByTitle
from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify

blp = Blueprint('user_book', __name__, description="Books seen by user")


@blp.route('/book-seen-by-user')
class UserSeenBooks(MethodView):
	def __init__(self):
		self.user_data = LibraryUserDataBase()
		self.books_data = LibraryBooksDataBase()

	@blp.arguments(UserBookSeen)
	def post(self, request_data):
		user_name = request_data['name']
		user_email = request_data['email']
		row = self.user_data.get_user()
		for data in row:
			if data['name'] == user_name and data['email'] == user_email:
				books = self.books_data.get_books()
				return books, 200
		return jsonify({
			"description": "Please register first...",
			"error": "user data not match in record...."
		}), 404


@blp.route('/user-seen-book-by-book-name')
class UserSeenBooks(MethodView):
	def __init__(self):
		self.user_data = LibraryUserDataBase()
		self.books_data = LibraryBooksDataBase()

	@blp.arguments(UserBookSeenByTitle)
	def post(self, request_data):
		user_name = request_data['name']
		user_email = request_data['email']
		books_name = request_data['BooksTitle']
		user_row = self.user_data.get_user()
		user_data = next(
			(userdata for userdata in user_row if userdata['name'] == user_name and userdata['email'] == user_email),
			None)
		if user_data is None:
			return {
				"error": "record_not_found",
				"description": "Please register first."

			}, 404
		books_row = self.books_data.get_books()
		books_data = next(
			(bookdata for bookdata in books_row if bookdata['BooksTitle'] == books_name),
			None)
		if books_data is None:
			return {"message": f"The book '{books_name}' is not available."}, 404
		book_details = self.books_data.books_get_through_name(books_name)
		return jsonify(book_details), 200
