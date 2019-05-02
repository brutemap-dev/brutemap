#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

from lib.core import findElement
from lib.core import getCssSelector
from lib.core import getFormElements
from lib.data import SETTING

def getPasswordField(form):
    """
    Mendapatkan bidang ``password`` admin.
    """

    return findElement(form, getCssSelector("password"))

def getUserField(form):
    """
    Mendapatkan bidang ``user`` admin.
    """

    userField = findElement(form, getCssSelector("text"))
    if not userField:
        userField = findElement(form, getCssSelector("email"))
        if userField and not SETTING.IS_EMAIL_AUTHENTICATION:
            SETTING.IS_EMAIL_AUTHENTICATION = True

    return userField

def getValidForm(form_elements):
    """
    Mendapatkan ``form`` element, yang menuju ke dashboard situs.
    """

    for form in form_elements:
        passwordField = getPasswordField(form)
        if passwordField is not None:
            userField = getUserField(form)
            if userField is not None:
                # standard login page
                return form, userField, passwordField
            else:
                # web shell login page
                return form, userField, passwordField
        else:
            userField = getUserField(form)
            if userField is not None:
                # slide login page
                return form, userField, passwordField

def getFormField():
    """
    Mendapatkan bidang ``form`` valid
    """

    form_elements = getFormElements()
    return getValidForm(form_elements)
