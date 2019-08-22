from flask import jsonify, g

from app.libs.error_code import CreateSuccess, NotFound, Success, Forbidden
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User
from app.validators.forms import RegisterForm, UuidForm, UserInfoForm
from app import redis as rd

api = Redprint('user')


@api.route('/<string:username>', methods=['GET'])
@auth.login_required
def get_user_api(username):
    user = User.get_user_by_username(username)
    if not user:
        raise NotFound()
    return jsonify({
        'code': 0,
        'data': {
            'user': user
        }
    })


@api.route('/', methods=['POST'])
def register_user_api():
    form = RegisterForm().validate_for_api()
    _verification(form.uuid.data)
    User.register(form.username.data, form.password.data)
    return CreateSuccess('register successful')


@api.route('/', methods=['PUT'])
def modify_user_api():
    form = UserInfoForm().validate_for_api()
    data = {
        'nickname': form.nickname.data,
        'gender': form.gender.data,
        'college': form.college.data,
        'profession': form.profession.data,
        'class_': form.class_.data,
        'phone': form.phone.data,
        'qq': form.qq.data
    }
    User.modify(form.username.data, **data)
    return Success('Modify user success')


@api.route('/activation', methods=['POST'])
@auth.login_required
def activate_user_api():
    form = UuidForm().validate_for_api()
    _verification(form.uuid.data)
    User.modify(g.user.username, permission=1)
    return Success('activate success')


def _verification(uuid):
    if not int(rd.hget(uuid, 'success').decode('utf8')):
        raise Forbidden()
    rd.delete(uuid)
