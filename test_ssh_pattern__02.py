# Polishing of the base example

import unittest

from ssh_pattern import SSHClient


class SSHPatternTestCase(unittest.TestCase):
    def setUp(self):
        print("!!!! Running setUp")
        self.result = SSHClient().discover()

    def tearDown(self):
        print("!!!! Running tearDown / just for example")

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