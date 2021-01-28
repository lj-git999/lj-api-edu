# Create your views here.

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from course.models import CourseCategory, Course, CourseChapter
from course.serializer import CourseCategoryModelSerializer, CourseModelSerializer, CourseChapterModelSerializer, \
    CourseDetailModelSerializer
from user.pagination import CoursePageNumberPagination


class CourseCategoryAPIView(ListAPIView):
    """课程分类信息查询"""
    queryset = CourseCategory.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseCategoryModelSerializer


class CourseAPIView(ListAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ("course_category",)

    ordering_fields = ("id", "students", "price")

    pagination_class = CoursePageNumberPagination


class CourseDetailsAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseDetailModelSerializer


class CourseChapterAPIView(ListAPIView):
    queryset = CourseChapter.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseChapterModelSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields=["course"]
