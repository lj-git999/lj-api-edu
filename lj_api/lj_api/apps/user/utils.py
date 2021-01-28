from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from user.models import UserInfo


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "username": user.username,
        'user_id': user.id,
        'password': user.password,
    }


def get_user_by_account(account):
    try:
        user = UserInfo.objects.filter(Q(username=account) | Q(phone=account) | Q(email=account)).first()
    except UserInfo.DoesNotExist:
        return None
    else:
        return user


class UserAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        根据账号获取用户对象
        :param request:
        :param username: 前端输入的用户名，手机号 密码
        :param password:
        :param kwargs:
        :return: 查询出用户
        """
        user = get_user_by_account(username)
        if user and user.check_password(password) and user.is_authenticated:
            return user
        return None
