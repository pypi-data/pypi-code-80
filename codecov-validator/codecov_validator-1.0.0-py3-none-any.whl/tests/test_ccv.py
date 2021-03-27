import unittest
from unittest.mock import patch

import requests
from click.testing import CliRunner

from codecov_validator import ccv
from codecov_validator.ccv import NOT_OK, OK

invalid_file = """
codecovs:
token: "<some token here>"
bot: "codecov-io"
"""


# Test valid example file from
# [documentation](https://docs.codecov.io/docs/codecovyml-reference).
valid_file = """
codecov:
  token: "<some token here>"
  bot: "codecov-io"
  ci:
    - "travis.org"
  strict_yaml_branch: "yaml-config"
  max_report_age: 24
  disable_default_path_fixes: no
  require_ci_to_pass: yes
  notify:
    after_n_builds: 2
    wait_for_ci: yes
"""


class CcvTest(unittest.TestCase):
    def test_passing(self):
        self.assertEqual(1, 1)

    @patch("requests.post")
    def test_run_request_post_exception(self, post_mock):
        # the post commmand is tested for a list of different exceptions
        except_list = [
            requests.exceptions.ConnectTimeout,
            requests.exceptions.HTTPError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ]
        for except_element in except_list:
            # subtests are used to distinguish iterations
            with self.subTest(i=except_element):
                post_mock.side_effect = except_element
                with self.assertRaises(SystemExit) as cm:
                    ccv.run_request(valid_file)
                # check if the exit(1) was called
                self.assertEqual(cm.exception.code, NOT_OK)
                self.assertNotEqual(cm.exception.code, OK)

    def test_run_request_valid_file(self):
        received = ccv.run_request(valid_file)
        self.assertIn("Valid!", received)

    def test_run_request_invalid_file(self):
        received = ccv.run_request(invalid_file)
        self.assertIn("Wrong key", received)

    def test_open_file_invalid_filename(self):
        invalid_filename = "invalid_codecov.yml"
        with self.assertRaises(SystemExit) as cm:
            ccv.open_file(invalid_filename)
        self.assertEqual(cm.exception.code, NOT_OK)

    def test_open_file_valid_filename(self):
        right_filename = "codecov.yml"
        received = ccv.open_file(right_filename)
        self.assertIs(type(received), bytes)

    def test_check_valid_valid_input(self):
        valid_input = "Valid!"
        with self.assertRaises(SystemExit) as cm:
            ccv.check_valid(valid_input)
        self.assertEqual(cm.exception.code, OK)
        self.assertNotEqual(cm.exception.code, NOT_OK)

    def test_check_valid_invalid_input(self):
        invalid_input = "Invalid!"
        with self.assertRaises(SystemExit) as cm:
            ccv.check_valid(invalid_input)
        self.assertEqual(cm.exception.code, NOT_OK)
        self.assertNotEqual(cm.exception.code, OK)

    def test_ccv_valid_clirunner(self):
        runner = CliRunner()
        result = runner.invoke(ccv.ccv)
        self.assertEqual(result.exit_code, OK)


if __name__ == "__main__":
    unittest.main()
