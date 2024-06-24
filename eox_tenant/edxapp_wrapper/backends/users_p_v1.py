"""Palm backend user module."""
from common.djangoapps.student.models.user import UserSignupSource  # pylint: disable=import-error


def get_user_signup_source():
    """Allow to get the model UserSignupSource from
    https://github.com/openedx/edx-platform/blob/open-release/palm.master/common/djangoapps/student/models/user.py#L820

    Returns:
        UserSignupSource model.
    """
    return UserSignupSource
