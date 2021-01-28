import re

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user.models import UserInfo
from user.utils import get_user_by_account


class UserModelSerializer(ModelSerializer):
    token = serializers.CharField(max_length=1024, read_only=True, help_text="用户token")
    code = serializers.CharField(max_length=6, write_only=True, help_text="短信验证码")

    class Meta:
        model = UserInfo
        fields = ["password", "username", "phone", "token", "id", "code"]
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
            "phone": {
                "write_only": True
            },
            "username": {
                "read_only": True
            },
            "id": {
                "read_only": True
            }
        }

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")
        code = attrs.get("code")
        print(password, type(code), code)
        print(phone)
        if not re.match(r"^(13[0-9]|14[01456879]|15[0-3,5-9]|16[2567]|17[0-8]|18[0-9]|19[0-3,5-9])\d{8}$", phone):
            raise serializers.ValidationError("手机号格式错误")

        try:
            user = get_user_by_account(phone)
            print(user)
        except UserInfo.DoesNotExist:
            user = None
        if user:
            raise serializers.ValidationError("手机号已经被注册")
        # 验证密码格式
        if not re.match(r"^[a-zA-Z\d_]{8,16}$", password):
            print(password)
            raise serializers.ValidationError("密码格式错误")
        redis_connection = get_redis_connection("sms_code")
        phone_code = redis_connection.get("exp_%s" % phone)
        print(phone_code)
        if phone_code.decode() != code:
            print(phone_code.decode())
            raise serializers.ValidationError("验证码输入错误")

        return attrs

    def create(self, validated_data):
        password = validated_data.get("password")
        hash_pwd = make_password(password)
        username = validated_data.get("phone")
        print(username, hash_pwd)
        user_obj = UserInfo.objects.create(
            username=username,
            password=hash_pwd,
            phone=username,
        )
        """为注册成功的用户生成token"""
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER

        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user_obj)
        user_obj.token = jwt_encode_handler(payload)
        return user_obj


class LoginModelSerializer(ModelSerializer):
    code = serializers.CharField(max_length=6, write_only=True, help_text="短信验证码")
    token = serializers.CharField(max_length=1024, read_only=True, help_text="用户token")
    account = serializers.CharField(write_only=True)

    class Meta:
        model = UserInfo
        fields = ["phone", "code", "token", "id", "account"]
        extra_kwargs = {
            "id": {
                "read_only": True
            },
            "phone": {
                "read_only": True
            }
        }

    def validate(self, attrs):
        print(123)
        phone = attrs.get("account")
        code = attrs.get("code")
        print(code, phone)
        try:
            user = get_user_by_account(phone)
            print(user)
        except UserInfo.DoesNotExist:
            user = None
        if not user:
            raise serializers.ValidationError("此手机号没有被注册")
        redis_connection = get_redis_connection("sms_code")
        phone_code = redis_connection.get("exp_%s" % phone)
        print(phone_code)
        if phone_code.decode() != code:
            raise serializers.ValidationError("验证码错误")

        user_obj = UserInfo.objects.get(phone=phone)
        print(user_obj)
        if user_obj and phone_code.decode() == code:
            from rest_framework_jwt.settings import api_settings
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER

            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            self.obj = user_obj
            self.token = token

        return attrs
