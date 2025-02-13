from flask import request, jsonify
from Library_Backend_Api.Data_Base.user_data_base import LibraryUserDataBase
from flask.views import MethodView
from flask_smorest import Blueprint
import hashlib
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, set_access_cookies, unset_jwt_cookies
from Library_Backend_Api.Resources.ADMIN.blocklist import BLOCKLIST
from datetime import timedelta

blp = Blueprint('admin', __name__, description="Only For Admin")


@blp.route("/login")
class AdminLogin(MethodView):
	def __init__(self):
		self.user_data = LibraryUserDataBase()

	def post(self):
		request_data = request.get_json()
		admin_name = request_data['name']
		admin_password = request_data['pashword_hash']
		hash_password = hashlib.sha256(admin_password.encode('utf-8')).hexdigest()
		user = self.user_data.get_user_through_name(admin_name)
		if user[0]['name'] == admin_name and user[0]['pashword_hash'] == hash_password:
			access_token = create_access_token(identity=admin_name,expires_delta=timedelta(hours=24))
			response = jsonify({"message": "Login Successfully"})
			set_access_cookies(response, access_token)
			return response, 200
		return jsonify({"message": "Invalid Credentials...."}), 401


@blp.route('/logout')
class AdminLogout(MethodView):
	def __init__(self):
		self.user_data = LibraryUserDataBase()

	@jwt_required()
	def post(self):
		jti = get_jwt()['jti']
		BLOCKLIST.add(jti)
		response = jsonify({"message": "Logged out successfully...."})
		unset_jwt_cookies(response)
		return response, 200
