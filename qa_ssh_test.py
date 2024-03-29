# Abstract example of end-to-end test that QA would write

from subprocess import check_output

if __name__ == "__main__":
    res = check_output(["python", "ssh_pattern.py"])
    expected = b"Discovered software:\r\n * version            = 8.0p1\r\n * name               = OpenSSH for Windows\r\n * type               = SSH Client\r\nDetails:\r\n * library            = LibreSSL 2.6.5\r\n * hosts number       = 2\r\n\r\n"
    assert res == expected
    print(".")
