from flask import Flask
from Library_Backend_Api.Resources.ADMIN.admin_books import blp as BooksBluePrint
from Library_Backend_Api.Resources.ADMIN.admin_user import blp as AdminUserBluePrint
from Library_Backend_Api.Resources.ADMIN.admin import blp as AdminBluePrint
from Library_Backend_Api.Resources.Member.books_borrowed import blp as UserBookBorrow
from Library_Backend_Api.Resources.USER.user import blp as UserBluePrint
from Library_Backend_Api.Resources.USER.user_books import blp as UserBooksBluePrint
from flask_smorest import Api
from Library_Backend_Api.Resources.ADMIN.blocklist import BLOCKLIST
from flask_jwt_extended import JWTManager, unset_jwt_cookies
from flask_mail import Mail
import cloudinary
# from Library_Backend_Api.Resources.CHATBOT.chatbot import blp as BlueprintChatbot

from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=["http://localhost:63342"], supports_credentials=True)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['API_TITLE'] = 'books backend api'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = "/"
app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"
app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config['JWT_SECRET_KEY'] = "@#$^**784646467$%^$*##^##Y&#^#4564&*&^TU"

# JWT configuration for cookies
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config["JWT_COOKIE_SAMESITE"] = 'None'
app.config['JWT_COOKIE_HTTPONLY'] = True

# cloudinary config
cloudinary.config(
	cloud_name="dofbbfgg4",
	api_key="596269484844184",
	api_secret="0uzI8tt4-bGFwAZuTfOiEMEQD2o"
)

# Access the value of an environment variable


app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "ht728350@gmail.com"
app.config['MAIL_PASSWORD'] = "hnzx xeiq sqcj vglh"
api = Api(app)
jwt = JWTManager(app)
mail_ = Mail(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jte_header, jwt_payload):
	return jwt_payload['jti'] in BLOCKLIST


@jwt.revoked_token_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
	return (
		{"description": "User has been logged out....",
		 'error': 'token_revoked'}
	), 401


@app.after_request
def unset_jwt(response):
	if response.status_code == 401:
		unset_jwt_cookies(response)
	return response


api.register_blueprint(BooksBluePrint)
api.register_blueprint(AdminUserBluePrint)
api.register_blueprint(AdminBluePrint)
api.register_blueprint(UserBluePrint)
api.register_blueprint(UserBooksBluePrint)
api.register_blueprint(UserBookBorrow)


if __name__ == "__main__":
	app.run(debug=True)
