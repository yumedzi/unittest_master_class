import re
import sys
from dataclasses import dataclass

from main import Software, emulate_long_running, logger, set_logger


@dataclass
class SSHClient(Software):
    emulated_delay: int = 0

    def get_type(self):
        return "SSH Client"

    def get_version(self):
        raw_text = self.run_cmd("ssh -V", delay=self.emulated_delay)

        return re.search(r"[_ ](\d[\w\.]*)", raw_text).group(1)

    def get_name(self):
        raw_text = self.run_cmd("ssh -V", delay=self.emulated_delay)

        return " ".join(
            re.search(r"^([a-zA-Z_ ]+)", raw_text, re.I).group(1).split("_")
        ).rstrip(" _")

    def get_details(self):
        # Get Library version
        raw_text = self.run_cmd("ssh -V", delay=self.emulated_delay)
        lib_info = re.search(r", ([\w \.]+)", raw_text).group(1)

        # Get number of known-hosts
        raw_file = self.get_file(r"~\.ssh\ssh_config", delay=self.emulated_delay)
        hosts_count = raw_file.count("Host ")

        return {"library": lib_info, "hosts number": hosts_count}


if __name__ == "__main__":
    set_logger(sys.argv, logger)
    print(SSHClient().discover())
