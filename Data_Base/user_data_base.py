import pyodbc


class LibraryUserDataBase:
	def __init__(self):
		self.conn = pyodbc.connect('DRIVER={SQL Server};Server=HACK_IT_NOW123;DATABASE=Library Management;')
		self.cursor = self.conn.cursor()

	def add_user(self, user_data):
		try:
			query = "INSERT INTO users(id,name,email,role) Values(?,?,?,?)"
			self.cursor.execute(query, (user_data['id'], user_data['name'], user_data['email'], user_data['role']))
			self.conn.commit()
			return "Successfully user added...."
		except Exception as e:
			return str(e)

	def get_user(self):
		user_list = []
		query = 'SELECT * FROM users'
		self.cursor.execute(query)
		for row in self.cursor.fetchall():
			user_dict = {'id': row[0], 'name': row[1], 'email': row[2], 'role': row[3], 'pashword_hash': row[4]}
			user_list.append(user_dict)
		return user_list

	def get_user_through_name(self, user_name):
		query = "SELECT * FROM users WHERE name =? "
		self.cursor.execute(query, (user_name,))
		row = self.cursor.fetchone()
		if row:
			user_dict = {'id': row[0], 'name': row[1], 'email': row[2], 'role': row[3], 'pashword_hash': row[4]}
			return [user_dict]
		else:
			return None

	def delete_user(self, user_email):
		query = "DELETE FROM users WHERE email=?"
		self.cursor.execute(query, (user_email,))
		if self.cursor.rowcount == 0:
			return False
		else:
			self.conn.commit()
			return True
