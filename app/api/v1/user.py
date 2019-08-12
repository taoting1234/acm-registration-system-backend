from flask import jsonify, g

from app.libs.error_code import CreateSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User
from app.validators.forms import RegisterForm

api = Redprint('user')


@api.route('', methods=['GET'])
@auth.login_required
def get_current_user_api():
    user = g.user
    return jsonify({
        'user': user
    })


@api.route('/<string:username>', methods=['GET'])
@auth.login_required
def get_user_api(username):
    user = User.get_user_by_username(username)
    return jsonify({
        'user': user
    })


@api.route('', methods=['POST'])
def create_user_api():
    form = RegisterForm().validate_for_api()
    User.register(form.username.data, form.password.data, form.nickname.data)
    return CreateSuccess('register user successful')