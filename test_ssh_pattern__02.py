# Polishing of the base example

import unittest


from ssh_pattern import SSHClient


class SSHPatternTestCase(unittest.TestCase):
    def setUp(self):
        self.result = SSHClient().discover()

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