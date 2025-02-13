import pyodbc


class BorrowBook:
	def __init__(self):
		self.conn = pyodbc.connect('DRIVER={SQL Server};Server=HACK_IT_NOW123;DATABASE=Library Management;')
		self.cursor = self.conn.cursor()

	def book_borrow(self, book_borrow_id, user_id, username_, bookname_, borrow_date, return_date_):
		try:
			query = "INSERT INTO Borrowed_Books(book_id,userid,username,bookname,borrow_date,return_date) Values(?,?,?,?,?,?)"
			self.cursor.execute(query, (book_borrow_id, user_id, username_, bookname_, borrow_date, return_date_))
			self.conn.commit()
		except Exception as e:
			return str(e)

	def get_borrow_book_data(self):
		borrowed_book_list = []
		query = "SELECT * FROM Borrowed_Books"
		self.cursor.execute(query)
		for row in self.cursor.fetchall():
			borrow_book_dict = {'book_id': row[0], 'userid': row[1], 'username': row[2], 'bookname': row[3],
			                    'borrow_date': row[4], 'return_date': row[5], 'fine': row[6]}
			borrowed_book_list.append(borrow_book_dict)
		return borrowed_book_list

	def get_borrow_book_data_id(self, student_id, book_title):
		query = "SELECT * FROM Borrowed_Books WHERE userid=? and bookname=?"
		self.cursor.execute(query, (student_id, book_title))
		student_data = self.cursor.fetchone()
		student_data_dict = {"book_id": student_data[0], "userid": student_data[1],
		                     "username": student_data[2], "bookname": student_data[3],
		                     "borrow_date": student_data[4],
		                     "return_date": student_data[5], "fine": student_data[6]}
		return [student_data_dict]

	def update_borrow_book_data_fine(self, user_id, amount, book_name):
		query = "UPDATE Borrowed_Books SET fine=? WHERE userid=? and bookname=?"
		self.cursor.execute(query, (amount, user_id, book_name))
		self.conn.commit()

	def update_return_date_and_issue_date(self, returndate, issuedate, user_id, book_name):
		query = "UPDATE Borrowed_Books SET return_date=?, borrow_date=? WHERE userid=? and bookname=?"
		self.cursor.execute(query, (returndate, issuedate, user_id, book_name))
		self.conn.commit()

	def delete_borrow_book_data(self, userid_, book_name):
		query = "DELETE from Borrowed_Books where userid=? and bookname=?"
		self.cursor.execute(query, (userid_, book_name))
		if self.cursor.rowcount == 0:
			return False
		else:
			self.conn.commit()
			return True
