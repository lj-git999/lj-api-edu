from django.urls import path

from course import views

urlpatterns = [
    path("list/", views.CourseAPIView.as_view()),
    path("category/", views.CourseCategoryAPIView.as_view()),
    path("detail/<str:pk>/", views.CourseDetailsAPIView.as_view()),
    path("chapter/", views.CourseChapterAPIView.as_view()),
]
