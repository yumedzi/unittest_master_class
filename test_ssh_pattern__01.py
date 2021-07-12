# Basic start example of unit tests

import unittest


from ssh_pattern import SSHClient


class SSHPatternTestCase(unittest.TestCase):
    def test_01_normal_run_name(self):
        res = SSHClient().discover()
        self.assertEqual(res.name, "OpenSSH for Windows")

    def test_02_normal_run_type(self):
        res = SSHClient().discover()
        self.assertEqual(res.type, "SSH Client")

    def test_03_normal_run_version(self):
        res = SSHClient().discover()
        self.assertEqual(res.version, "8.0p1")

    def test_04_normal_run_details(self):
        res = SSHClient().discover()
        self.assertEqual(res.details, {"library": "LibreSSL 2.6.5", "hosts number": 2})


if __name__ == "__main__":
    unittest.main()