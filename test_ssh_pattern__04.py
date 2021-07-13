# Adding mocks

import unittest
from unittest.mock import MagicMock

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


if __name__ == "__main__":
    unittest.main()