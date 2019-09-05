""" Backend for course enrollments. """
from student import models  # pylint: disable=import-error


def get_enrollments_model():
    """ Get course enrollment model object from the platform. """
    return models.CourseEnrollment


def get_enrollments_model_manager():
    """ Get course enrollment model manager object from the platform. """
    return models.CourseEnrollmentManager
