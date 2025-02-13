import pyodbc
from flask import jsonify


class LibraryBooksDataBase:
	def __init__(self):
		self.conn = pyodbc.connect('DRIVER={SQL Server};Server=HACK_IT_NOW123;DATABASE=Library Management;')
		self.cursor = self.conn.cursor()

	def add_books(self, bookid, request_datas, image_url):

		try:
			query = "INSERT INTO Books(id,BooksTitle,author,genre,published_date,available_copies,books_image_url) VALUES (?,?,?,?,?,?,?);"
			self.cursor.execute(query, (
				bookid, request_datas['BooksTitle'], request_datas['author'], request_datas['genre'],
				request_datas['published_date'], request_datas['available_copies'], image_url))
			self.conn.commit()
			return {"message": "added successfully........"}
		except Exception as error:
			print(str(error))

	def get_books(self):
		try:
			book_list = []
			query = "SELECT * FROM Books"
			self.cursor.execute(query)
			for row in self.cursor.fetchall():
				print(row[6])
				books_dict = {'id': row[0], 'BooksTitle': row[1], 'author': row[2], 'genre': row[3],
				              'published_date': row[4],
				              'available_copies': row[5],
				              'books_image_url': row[6] if row[6] else "https://via.placeholder.com/60x80"}

				book_list.append(books_dict)
			return book_list
		except Exception as e:
			return str(e)

	def books_get_through_name(self, book_name):
		try:
			query = "SELECT * FROM Books WHERE BooksTitle=?;"
			self.cursor.execute(query, (book_name,))
			books_ = self.cursor.fetchone()
			if books_:
				books_dict = {
					'id': books_[0],
					'BooksTitle': books_[1],
					'author': books_[2],
					'genre': books_[3],
					'published_date': books_[4],
					'available_copies': books_[5],
					'books_image_url': books_[6] if books_[6] else "https://via.placeholder.com/60x80"}

				return books_dict
			else:
				return None
		except Exception as error:

			return str(error)

	def update_books(self, available_copy, books_name):
		try:
			query = "UPDATE Books SET available_copies = ? WHERE BooksTitle = ?; "
			self.cursor.execute(query, (available_copy, books_name))
			self.conn.commit()
			return {"message": 'update successfully....'}
		except Exception as error:
			self.conn.rollback()
			return str(error)

	def delete_books(self, books_name):
		query = "DELETE FROM Books WHERE BooksTitle=?"
		self.cursor.execute(query, (books_name,))
		if self.cursor.rowcount == 0:
			return False
		else:
			self.conn.commit()
			return True
