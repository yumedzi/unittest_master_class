# Adding more tests using mocked data

import unittest
from unittest.mock import patch, MagicMock

from ssh_pattern import SSHClient
from main import Software


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
        self.assertEqual(self.result.name, "OpenSSH for Windows")

    def test_02_normal_run_type(self):
        self.assertEqual(self.result.type, "SSH Client")

    def test_03_normal_run_version(self):
        self.assertEqual(self.result.version, "8.0p1")

    def test_04_normal_run_details(self):
        self.assertEqual(
            self.result.details, {"library": "LibreSSL 2.6.5", "hosts number": 2}
        )

    def test_11_versioning(self):
        test_data = "OpenSSH_for_Windows_8.0p5, LibreSSL 2.6.5"
        expected = "8.0p5"

        with patch.object(SSHClient, "run_cmd", return_value=test_data):
            result = SSHClient(emulated_delay=5).get_version()
            self.assertEqual(result, expected)

    def test_12_versioning(self):
        test_data = "OpenSSH_for_Windows_7.3p05, LibreSSL 2.6.5"
        expected = "7.3p05"

        with patch.object(SSHClient, "run_cmd", return_value=test_data):
            result = SSHClient(emulated_delay=5).get_version()
            self.assertEqual(result, expected)

    def test_13_versioning(self):
        test_data = "OpenSSH_for_Windows_9, LibreSSL 2.6.5"
        expected = "9"

        with patch.object(SSHClient, "run_cmd", return_value=test_data):
            result = SSHClient(emulated_delay=5).get_version()
            self.assertEqual(result, expected)

    def test_14_versioning(self):
        test_data = "OpenSSH_for_Windows_7.7beta, LibreSSL 2.6.5"
        expected = "7.7beta"

        with patch.object(SSHClient, "run_cmd", return_value=test_data):
            result = SSHClient(emulated_delay=5).get_version()
            self.assertEqual(result, expected)

    def test_15_versioning(self):
        test_data = "Command not found"
        expected = ""

        with patch.object(SSHClient, "run_cmd", return_value=test_data):
            result = SSHClient(emulated_delay=5).get_version()
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()