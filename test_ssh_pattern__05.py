import unittest
from unittest.mock import patch, MagicMock

# Change emulate_long_running paramater to non-zero value

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
        self.assertEqual("OpenSSH for Windows", self.result.name)

    def test_02_normal_run_type(self):
        self.assertEqual("SSH Client", self.result.type)

    def test_03_normal_run_version(self):
        self.assertEqual("8.0p1", self.result.version)

    def test_04_normal_run_details(self):
        self.assertEqual(
            {"library": "LibreSSL 2.6.5", "hosts number": 2}, self.result.details
        )

    def test_11_versioning(self):
        test_data = "OpenSSH_for_Windows_8.0p5, LibreSSL 2.6.5"
        expected = "8.0p5"

        with patch.object(SSHClient, "run_cmd", return_value=test_data) as mock_method:
            result = SSHClient(emulated_delay=5).get_version()
            self.assertEqual(expected, result)

    def test_12_versioning(self):
        test_data = "OpenSSH_for_Windows_7.3p05, LibreSSL 2.6.5"
        expected = "7.3p05"

        with patch.object(SSHClient, "run_cmd", return_value=test_data) as mock_method:
            result = SSHClient(emulated_delay=5).get_version()
            self.assertEqual(expected, result)

    def test_13_versioning(self):
        test_data = "OpenSSH_for_Windows_9, LibreSSL 2.6.5"
        expected = "9"

        with patch.object(SSHClient, "run_cmd", return_value=test_data) as mock_method:
            result = SSHClient(emulated_delay=5).get_version()
            self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()