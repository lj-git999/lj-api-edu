from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django_redis import get_redis_connection
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from course.models import Course
from lj_api.settings.constants import IMG_SRC


class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def add_cart(self, request):
        course_id = request.data.get("course_id")
        # 获取用户id
        user_id = request.user.id
        print(user_id, course_id)
        select = True
        expire = 0
        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({
                "message": "参数有误，课程不存在"
            }, status=status.HTTP_400_BAD_REQUEST)
        # 存到redis
        try:
            redis_connection = get_redis_connection("cart")
            pipeline = redis_connection.pipeline()
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            pipeline.sadd("selected_%s" % user_id, course_id)
            pipeline.execute()
            cart_len = redis_connection.hlen("cart_%s" % user_id)
        except:
            return Response({
                "message": "参数有误，购物车添加失败"
            }, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        return Response({
            "message": "购物车添加成功",
            "cart_length": cart_len,

        }, status=status.HTTP_200_OK)

    def cart_list(self, request):
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")
        cart_list_byte = redis_connection.hgetall("cart_%s" % user_id)
        select_list_byte = redis_connection.smembers("selected_%s" % user_id)
        data = []
        for course_id_byte, expire_id_byte in cart_list_byte.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            try:
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue
            data.append({
                "selected": True if course_id_byte in select_list_byte else False,
                "course_img": IMG_SRC + course.course_img.url,
                "name": course.name,
                "id": course.id,
                "expire_id": expire_id,
                "price": course.price,
            })
        return Response(data)

    def change_select(self, request):
        user_id = request.user.id
        course_id = request.data.get("course_id")
        selected = request.data.get("selected")
        print(user_id, type(user_id))
        redis_connection = get_redis_connection("cart")
        if selected:
            redis_connection.sadd("selected_%s" % user_id, course_id)
        else:
            redis_connection.srem("selected_%s" % user_id, course_id)
        return Response({
            "message": "更改成功"
        }, status=status.HTTP_200_OK)

    def delete_cart(self, request):
        user_id = request.user.id
        course_id = request.data.get("course_id")
        print(user_id,course_id)
        redis_connection = get_redis_connection("cart")
        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({
                "message": "参数有误，课程不存在"
            }, status=status.HTTP_400_BAD_REQUEST)
        redis_connection.hdel("cart_%s" % user_id, course_id)
        cart_len=redis_connection.hlen("cart_%s"%user_id)
        return Response({
            "message":"删除课程成功",
            "cart_length":cart_len
        },status=status.HTTP_200_OK)
