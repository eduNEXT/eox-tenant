#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Users backend abstraction
"""
from student.models import UserSignupSource  # pylint: disable=import-error


def get_user_signup_source():
    """ get UserSignupSource model """
    return UserSignupSource
