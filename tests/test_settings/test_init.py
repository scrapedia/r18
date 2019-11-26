"""
TestCases for the functions and classes in the settings module
"""
import os
from unittest.case import TestCase
from unittest.mock import patch

from r18.exceptions import R18SettingsMissingException
from r18.settings import get_env_var


class SettingsFunctionsTest(TestCase):
    def test_get_env_var(self):
        with patch.dict(os.environ, {}):
            with self.assertRaises(R18SettingsMissingException):
                _ = get_env_var("NOT_EXIST")
            self.assertEqual(get_env_var("NOT_EXIST", default="VAL"), "VAL")
            self.assertEqual(get_env_var("NOT_EXIST", default=False), False)

        with patch.dict(os.environ, {"VAR": "VAL"}):
            self.assertEqual(get_env_var("VAR"), "VAL")
            self.assertEqual(get_env_var("VAR", default="OTHER_VAL"), "VAL")
            self.assertNotEqual(get_env_var("VAR", default="OTHER_VAL"), "OTHER_VAL")
