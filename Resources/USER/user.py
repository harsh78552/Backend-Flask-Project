from Library_Backend_Api.Data_Base.user_data_base import LibraryUserDataBase
from Library_Backend_Api.Data_Base.book_data_base import LibraryBooksDataBase
from Library_Backend_Api.Schemas.user_schema import UserAddSchema
from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify, request

blp = Blueprint('user', __name__, description="operation through user")


@blp.route('/register_user')
class RegisterUser(MethodView):
	def __init__(self):
		self.user_database = LibraryUserDataBase()

	@blp.arguments(UserAddSchema)
	def post(self, request_data):
		user = self.user_database.get_user_through_name(request_data['name'])
		if user and user[0]['email'] == request_data['email']:
			return {"message": 'user already registered....'}
		self.user_database.add_user(request_data)
		return {"message": 'user register successfully....'}
