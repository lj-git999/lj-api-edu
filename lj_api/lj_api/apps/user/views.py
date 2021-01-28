from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from lj_api.libs.geetest import GeetestLib
from lj_api.settings import constants
from lj_api.utils.random_code import get_random_code
from lj_api.utils.send_message import Message
from user.models import UserInfo
from user.serializer import UserModelSerializer, LoginModelSerializer

from user.utils import get_user_by_account

pc_geetest_id = "45dbe199c830b4b9cb1bebd76fbbfdb7"
pc_geetest_key = "cbdff4cfb81c08cb1312f36b963fec22"


class CaptchaAPIView(APIView):
    """极验验证码"""

    user_id = 0
    status = False

    def get(self, request, *args, **kwargs):
        """获取验证码"""

        # 根据用户名验证当前用户是否存在
        account = request.query_params.get("username")
        user = get_user_by_account(account)

        if user is None:
            return Response({"message": "用户不存在"}, status=status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        print(self.status)
        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self, request, *args, **kwargs):
        """校验验证码"""
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.data.get("geetest_challenge")
        validate = request.data.get("geetest_validate")
        seccode = request.data.get("geetest_seccode")
        account = request.data.get("username")
        user = get_user_by_account(account)
        print(user)
        if user:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)


# 注册逻辑视图
class UserAPIView(CreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer
    print(queryset)


# 短信验证码
class MessageAPIView(APIView):

    def get(self, request, *args, **kwargs):
        phone = request.query_params.get("phone")
        print(phone)
        redis_connection = get_redis_connection("sms_code")
        mobile = redis_connection.get("sms_%s" % phone)
        if mobile is not None:
            return Response({
                "message": "您已经在60s内发送过短信了",
            }, status=status.HTTP_400_BAD_REQUEST)
        code = get_random_code()
        print(code)
        redis_connection.setex("sms_%s" % phone, constants.SMS_EXPIRE_TIME, code)
        redis_connection.setex("exp_%s" % phone, constants.MOBILE_EXPIRE_TIME, code)
        # try:
        #     message = Message(constants.API_KEY)
        #     message.send_message(phone, code)
        # except:
        #     return Response({
        #         "message": "短信发送失败，请稍后再试"
        #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "message": "发送短信成功",
        }, status=status.HTTP_200_OK)


# 手机验证有没有被注册
class PhoneAPIView(APIView):
    def get(self, request, *args, **kwargs):
        phone = request.query_params.get("phone")
        print(phone)
        user = UserInfo.objects.filter(phone=phone)
        print(user)
        if user:
            return Response({
                "message": "手机号已注册"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                "message": "此手机号可用"
            }, status=status.HTTP_200_OK)


# 手机号登录视图
class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = LoginModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
        return Response({
            "user": LoginModelSerializer(serializer.obj).data,
            "token": serializer.token,
        })


# 登录 手机号校验逻辑
class PhoneVerifyAPIView(APIView):

    def get(self, request, *args, **kwargs):
        phone = request.query_params.get("phone")
        print(phone)
        user = UserInfo.objects.filter(phone=phone)
        print(user)
        if user:
            return Response({
                "message": "手机号已注册"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "此手机号没有注册，请先注册"
            }, status=status.HTTP_403_FORBIDDEN)
