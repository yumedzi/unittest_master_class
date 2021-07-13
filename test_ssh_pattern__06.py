# Optimizing tests

import unittest
from unittest.mock import patch, MagicMock

from ssh_pattern import SSHClient


class SSHPatternTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ssh = SSHClient(emulated_delay=5)

        ssh.run_cmd = MagicMock(
            return_value="OpenSSH_for_Windows_8.0p1, LibreSSL 2.6.5"
        )

        ssh.get_file = MagicMock(
            return_value="""Host dev_host
      HostName 1.2.3.4
      Port 8922
      User user

    Host prod_host
      HostName 1.2.3.4
      Port 22
      User root"""
        )

        cls.result = ssh.discover()

    def test_01_normal_run_name(self):
        self.assertEqual("OpenSSH for Windows", self.result.name)

    def test_02_normal_run_type(self):
        self.assertEqual("SSH Client", self.result.type)

    def test_03_normal_run_version(self):
        self.assertEqual("8.0p1", self.result.version)

    def test_04_normal_run_details(self):
        self.assertEqual(
            {"library": "LibreSSL 2.6.5", "hosts number": 2}, self.result.details
        )


class SSHPatternVersioningTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ssh = SSHClient(emulated_delay=5)

        # Patchers
        run_cmd_patcher = patch("ssh_pattern.SSHClient.run_cmd")
        get_file_patcher = patch("ssh_pattern.SSHClient.get_file")

        # Mocks
        cls.mock_methods = dict(
            run_cmd=run_cmd_patcher.start(), get_file=get_file_patcher.start()
        )

    @classmethod
    def tearDownClass(cls):
        patch.stopall()

    def run_test(self, mock_method, mock_value, expected):
        # Mock method is there?
        assert mock_method in self.mock_methods

        # Run a test using mocking data
        self.mock_methods[mock_method].return_value = mock_value
        res = self.ssh.discover()
        self.assertEqual(res.version, expected)

    def test_11_versioning(self):
        test_data = "OpenSSH_for_Windows_8.0p5, LibreSSL 2.6.5", "8.0p5"

        self.run_test("run_cmd", *test_data)

    def test_12_versioning(self):
        test_data = "OpenSSH_for_Windows_7.3p05, LibreSSL 2.6.5", "7.3p05"

        self.run_test("run_cmd", *test_data)

    def test_13_versioning(self):
        test_data = "OpenSSH_for_Windows_9, LibreSSL 2.6.5", "9"

        self.run_test("run_cmd", *test_data)

    def test_14_versioning(self):
        test_data = "OpenSSH_for_Windows_7.7beta, LibreSSL 2.6.5", "7.7beta"

        self.run_test("run_cmd", *test_data)

    def test_15_versioning(self):
        test_data = "Command not found", ""

        self.run_test("run_cmd", *test_data)


class SSHPatternNameTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ssh = SSHClient(emulated_delay=5)

        # Mocks
        run_cmd_patcher = patch("ssh_pattern.SSHClient.run_cmd")
        get_file_patcher = patch("ssh_pattern.SSHClient.get_file")

        cls.mock_methods = dict(
            run_cmd=run_cmd_patcher.start(), get_file=get_file_patcher.start()
        )

    @classmethod
    def tearDownClass(cls):
        patch.stopall()

    def run_test(self, mock_method, mock_value, expected):
        # Mock method is there?
        assert mock_method in self.mock_methods

        # Run a test using mocking data
        self.mock_methods[mock_method].return_value = mock_value
        res = self.ssh.discover()
        self.assertEqual(res.name, expected)

    def test_21_naming(self):
        test_data = "OpenSSH_for_Windows_8.0p5, LibreSSL 2.6.5", "OpenSSH for Windows"

        self.run_test("run_cmd", *test_data)

    def test_22_naming(self):
        test_data = "OpenSSH 7.3p05, LibreSSL 2.6.5", "OpenSSH"

        self.run_test("run_cmd", *test_data)

    def test_23_naming(self):
        test_data = "OpenSSH_for_Unix___9, LibreSSL 2.6.5", "OpenSSH for Unix"

        self.run_test("run_cmd", *test_data)


if __name__ == "__main__":
    unittest.main()