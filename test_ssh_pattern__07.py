# Organizing test cases via introducing the base test case class

import unittest
from unittest.mock import patch, MagicMock

from ssh_pattern import SSHClient


class SSHPatternBaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ssh = SSHClient(emulated_delay=5)

        # Mocks
        run_cmd_patcher = patch("ssh_pattern.SSHClient.run_cmd")
        get_file_patcher = patch("ssh_pattern.SSHClient.get_file")

        cls.mock_methods = dict(
            run_cmd=run_cmd_patcher.start(), get_file=get_file_patcher.start()
        )

        cls.addClassCleanup(patch.stopall)

    def run_test(self, mock_method, mock_value, expected):
        # Mock method is there?
        assert self.mock_method in self.mock_methods

        # Run a test using mocking data
        self.mock_methods[mock_method].return_value = mock_value
        res = self.ssh.discover()
        self.assertEqual(getattr(res, self.test_attribute), expected)


class SSHPatternVersioningTestCase(SSHPatternBaseTestCase):
    mock_method = "run_cmd"
    test_attribute = "version"

    def test_11_versioning(self):
        test_data = "OpenSSH_for_Windows_8.0p5, LibreSSL 2.6.5"
        expected = "8.0p5"

        self.run_test("run_cmd", test_data, expected)

    def test_12_versioning(self):
        test_data = "OpenSSH_for_Windows_7.3p05, LibreSSL 2.6.5"
        expected = "7.3p05"

        self.run_test("run_cmd", test_data, expected)

    def test_13_versioning(self):
        test_data = "OpenSSH_for_Windows_9, LibreSSL 2.6.5"
        expected = "9"

        self.run_test("run_cmd", test_data, expected)


class SSHPatternNameTestCase(SSHPatternBaseTestCase):
    mock_method = "run_cmd"
    test_attribute = "name"

    def test_21_naming(self):
        test_data = "OpenSSH_for_Windows_8.0p5, LibreSSL 2.6.5"
        expected = "OpenSSH for Windows"

        self.run_test("run_cmd", test_data, expected)

    def test_22_naming(self):
        test_data = "OpenSSH 7.3p05, LibreSSL 2.6.5"
        expected = "OpenSSH"

        self.run_test("run_cmd", test_data, expected)

    def test_23_naming(self):
        test_data = "OpenSSH_for_Unix___9, LibreSSL 2.6.5"
        expected = "OpenSSH for Unix"

        self.run_test("run_cmd", test_data, expected)


if __name__ == "__main__":
    unittest.main()