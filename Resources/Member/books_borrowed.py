from flask import request, jsonify
from Library_Backend_Api.Data_Base.user_data_base import LibraryUserDataBase
from Library_Backend_Api.Data_Base.book_data_base import LibraryBooksDataBase
from Library_Backend_Api.Data_Base.borrow_books import BorrowBook
from flask_smorest import Blueprint
from flask.views import MethodView
from Library_Backend_Api.id_generator import generate_id
from Library_Backend_Api.date_time_module import get_today_date, date_after_15_days, TotalDate
from flask_mail import Message
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta

blp = Blueprint("book-borrow", __name__, description="book issue by admin")


@blp.route('/book-issue')
class BookBorrowAdmin(MethodView):
	def __init__(self):
		self.user_data_base = LibraryUserDataBase()
		self.book_data_base = LibraryBooksDataBase()
		self.borrow_book_data = BorrowBook()
		self.date = TotalDate()

	@jwt_required()
	def post(self):
		from Library_Backend_Api.app_run import mail_
		request_data = request.get_json()
		username = request_data['name']
		book_title = request_data['BooksTitle']
		user_data = self.user_data_base.get_user_through_name(username)
		if user_data is None:
			return {"message": "User is not match in record...."}, 404
		book_data = self.book_data_base.books_get_through_name(book_title)
		if book_data is None:
			return {"message": "Book is not in record...."}, 404
		if book_data[0]['available_copies'] > 0:
			self.borrow_book_data.book_borrow(generate_id(), user_data[0]['id'], username,
			                                  book_title, get_today_date(), date_after_15_days())
			self.book_data_base.update_books(book_data[0]['available_copies'] - 1, book_data[0]['BooksTitle'])
			try:
				subject = "book submitted date.."
				recipient = user_data[0]['email']
				body = f"Book submitted on {date_after_15_days()}."
				msg = Message(subject=subject, sender="ht728350@gmail.com", recipients=[recipient])
				msg.body = body
				mail_.send(msg)
				return {"message": "Book issued successfully..."}
			except Exception as e:
				return str(e)
		return jsonify({"message": "All available_copies issued...."})


@blp.route("/book-reissue")
class BookReissue(MethodView):
	def __init__(self):
		self.borrow_book_data = BorrowBook()
		self.user_data_base = LibraryUserDataBase()

	def put(self):
		request_data = request.get_json()
		userid = request_data['userid']
		book_name = request_data['bookname']
		student_data = self.borrow_book_data.get_borrow_book_data_id(userid, book_name)
		user_data = self.user_data_base.get_user_through_name(student_data[0]['username'])
		date = student_data[0]['return_date']
		date1 = datetime.strptime(date, "%Y-%m-%d")
		date2 = datetime.strptime(get_today_date(), "%d %B %Y")
		day_difference = (date2 - date1).days
		fine = day_difference * 2 if day_difference > 0 else 0
		date_obj = datetime.strptime(get_today_date(), "%d %B %Y")
		new_date = date_obj + timedelta(days=15)
		new_date_str = new_date.strftime("%d %B %Y")
		self.borrow_book_data.update_return_date_and_issue_date(new_date_str, get_today_date(), userid,
		                                                        student_data[0]['bookname'])
		try:
			from Library_Backend_Api.app_run import mail_
			subject = "book submitted date.."
			recipient = user_data[0]['email']
			body = f"Book submitted on {new_date_str}."
			msg = Message(subject=subject, sender="ht728350@gmail.com", recipients=[recipient])
			msg.body = body
			mail_.send(msg)
			response_message = {"message": "Book re-issued successfully..."}
			if fine > 0:
				response_message['fine'] = f"{fine}₹ fine..."
			return jsonify(response_message), 200
		except Exception as e:
			return jsonify({"error": f"Email sending failed: {str(e)}"}), 500


@blp.route("/book-borrow-data")
class BorrowBookData(MethodView):
	def __init__(self):
		self.book_data = BorrowBook()

	def get(self):
		borrow_book_data = self.book_data.get_borrow_book_data()
		return jsonify(borrow_book_data)


@blp.route("/delete-student")
class DeleteStudent(MethodView):
	def __init__(self):
		self.student_data = BorrowBook()
		self.book_data_base = LibraryBooksDataBase()

	def delete(self):
		request_data = request.get_json()
		userid = request_data['userid']
		bookname = request_data['bookname']
		student_data = self.student_data.get_borrow_book_data_id(userid, bookname)
		book_data = self.book_data_base.books_get_through_name(bookname)
		date = student_data[0]['return_date']
		date1 = datetime.strptime(date, "%Y-%m-%d")
		date2 = datetime.strptime(get_today_date(), "%d %B %Y")
		day_difference = (date2 - date1).days
		fine = day_difference * 2 if day_difference > 0 else 0
		if self.student_data.delete_borrow_book_data(userid, bookname):
			self.book_data_base.update_books(book_data[0]['available_copies'] + 1, book_data[0]['BooksTitle'])
		response_message = {"message": "deleted successfully...."}
		if fine > 0:
			response_message['fine'] = f"{fine}₹ fine..."
		return jsonify(response_message), 200


