"""Lilac backend user module."""
try:
    from common.djangoapps.student.models import UserSignupSource
except ImportError:
    UserSignupSource = object


def get_user_signup_source():
    """Allow to get the model UserSignupSource from
    https://github.com/edx/edx-platform/blob/open-release/lilac.master/common/djangoapps/student/models.py#L849

    Returns:
        UserSignupSource model.
    """
    return UserSignupSource
