from Library_Backend_Api.Data_Base.user_data_base import LibraryUserDataBase
from Library_Backend_Api.Schemas.user_schema import UserSchema, UserOptionalSchema, UserAddSchema, UserDeleteSchema
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from flask import request

blp = Blueprint('admin_user', __name__, description="Operation through admin_user")


@blp.route('/admin-get-user-data')
class User(MethodView):
	def __init__(self):
		self.user_database = LibraryUserDataBase()

	@jwt_required()
	@blp.response(200, UserSchema(many=True))
	@blp.arguments(UserOptionalSchema, location='query')
	def get(self, args):
		user_name = args.get('name')
		if user_name is None:
			return self.user_database.get_user()
		else:
			result = self.user_database.get_user_through_name(user_name)
			if not result:
				abort(404, message='record not found...')
			return result


@blp.route("/admin-add-student")
class AdminJoinStudent(MethodView):
	def __init__(self):
		self.user_database = LibraryUserDataBase()

	@jwt_required()
	def post(self):
		request_data = request.get_json()
		self.user_database.add_user(request_data)
		return {"message": "user added successfully...."}


@blp.route("/admin-delete-student")
class DeleteStudent(MethodView):
	def __init__(self):
		self.user_database = LibraryUserDataBase()

	@jwt_required()
	# @blp.arguments(UserDeleteSchema)
	def delete(self):
		request_data = request.get_json()
		request_email = request_data['email']
		if self.user_database.delete_user(request_email):
			return {"message": "User deleted successfully..."}
		abort(404, message="record not found.....")
