# Emulating long running commands

import unittest
from unittest.mock import MagicMock

from ssh_pattern import SSHClient
from main import Software


class SSHPatternTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ssh = SSHClient(emulated_delay=3)
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


if __name__ == "__main__":
    unittest.main()