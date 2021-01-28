import xadmin

from course.models import CourseCategory, CourseLesson, Course, CourseChapter, Teacher


class CourseCategoryModelAdmin(object):
    """分类表"""
    pass


xadmin.site.register(CourseCategory,CourseCategoryModelAdmin)


class CourseModelAdmin(object):
    """课程表"""
    pass


xadmin.site.register(Course, CourseModelAdmin)


class CourseLessonModelAdmin(object):
    """课时表"""
    pass


xadmin.site.register(CourseLesson,CourseLessonModelAdmin)


class CourseChapterModelAdmin(object):
    """章节表"""

    pass


xadmin.site.register(CourseChapter,CourseChapterModelAdmin)


class TeacherModelAdmin(object):
    """讲师表"""
    pass


xadmin.site.register(Teacher, TeacherModelAdmin)
