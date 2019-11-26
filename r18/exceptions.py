"""
Exceptions used in this spider
"""


class R18Exception(Exception):
    """
    The root exception used in this spider
    """


class R18SettingsMissingException(R18Exception):
    """
    The necessary settings is missing
    """
