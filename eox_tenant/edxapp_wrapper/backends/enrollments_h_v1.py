""" backend """
from student import models  # pylint: disable=import-error


def get_enrollments_model():
    """ backend function """
    return models.CourseEnrollment


def get_enrollments_model_manager():
    """ backend function """
    return models.CourseEnrollmentManager
