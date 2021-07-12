import re
import sys
from dataclasses import dataclass

from main import Software, logger, set_logger


@dataclass
class DockerDesktop(Software):
    emulated_delay: int = 2

    def get_type(self):
        return "Docker Desktop"

    def get_version(self):
        raw_text = self.run_cmd("docker -v", delay=self.emulated_delay)
        return re.search(r"Docker version (\d[\w\.]+)", raw_text).group(1)

    def get_name(self):
        raw_text = self.run_cmd("docker info", delay=self.emulated_delay)
        return re.search(r"^\s+Name: ([\w\-]+)", raw_text, re.M).group(1)

    def get_details(self):
        # Get ID & containers count
        raw_text = self.run_cmd("docker info", delay=self.emulated_delay)
        id_info = re.search(r"^\s+ID: ((?:\w+:)+)", raw_text, re.M).group(1)
        containers_count = re.search(r"^\s+Containers: (\d+)", raw_text, re.M).group(1)

        # Get build id
        raw_file = self.get_file("~\.docker\.buildNodeID")
        build_id = raw_file

        # Count of dev envs
        raw_file = self.get_file(r"~\.docker\devenvironments\data.json")
        dev_envs_count = len(self.json(raw_file))

        return {
            "id": id_info,
            "build_id": build_id,
            "containers_count": containers_count,
            "dev_envs_count": dev_envs_count,
        }


if __name__ == "__main__":
    set_logger(sys.argv, logger)
    print(DockerDesktop().discover())