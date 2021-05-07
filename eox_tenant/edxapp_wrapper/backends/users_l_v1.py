"""Lilac backend user module."""
from common.djangoapps.student.models import UserSignupSource  # pylint: disable=import-error


def get_user_signup_source():
    """Allow to get the model UserSignupSource from
    https://github.com/edx/edx-platform/blob/open-release/lilac.master/common/djangoapps/student/models.py#L849

    Returns:
        UserSignupSource model.
    """
    return UserSignupSource
