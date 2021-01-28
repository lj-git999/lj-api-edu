from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Teacher, Course, CourseChapter, CourseLesson


class CourseCategoryModelSerializer(ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ["id", "name"]


class TeacherModelSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", "name", "title", "image", "brief", "signature"]


class CourseModelSerializer(ModelSerializer):
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher", "lesson_list", ]


class CourseDetailModelSerializer(ModelSerializer):
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher", "level_name",
                  "course_video","brief_html"]


class CourseLessonModelSerializer(ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ["id", "name", "duration", "free_trail"]


class CourseChapterModelSerializer(ModelSerializer):
    coursesections = CourseLessonModelSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ["id", "name", "chapter", "coursesections"]
