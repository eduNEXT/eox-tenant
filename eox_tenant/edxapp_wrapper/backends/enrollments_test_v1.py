""" Enrollments test backend """
from django.db import models


def get_enrollments_model():
    """ backend function """
    try:
        from student.models import CourseEnrollment
    except ImportError:
        CourseEnrollment = object
    return CourseEnrollment


def get_enrollments_model_manager():
    """ backend function """
    try:
        from student.models import CourseEnrollmentManager
    except ImportError:
        CourseEnrollmentManager = models.Manager
    return CourseEnrollmentManager
