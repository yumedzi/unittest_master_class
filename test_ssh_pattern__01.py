import unittest


from ssh_pattern import SSHClient


class SSHPatternTestCase(unittest.TestCase):
    def test_01_normal_run_name(self):
        res = SSHClient().discover()
        self.assertEqual("OpenSSH for Windows", res.name)

    def test_02_normal_run_type(self):
        res = SSHClient().discover()
        self.assertEqual("SSH Client", res.type)

    def test_03_normal_run_version(self):
        res = SSHClient().discover()
        self.assertEqual("8.0p1", res.version)

    def test_04_normal_run_details(self):
        res = SSHClient().discover()
        self.assertEqual({"library": "LibreSSL 2.6.5", "hosts number": 2}, res.details)


if __name__ == "__main__":
    unittest.main()