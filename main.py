# This is a helper module intended to provide a base abstract class - "Software"
# for the "Pattern" class.
# Pattern is class used to model some piece of software installed/running in the system,
# it is a subclass of Software which has some abstract methods required to be implemented.

import sys
from dataclasses import dataclass
from os.path import expanduser
from abc import ABC, abstractmethod
from subprocess import check_output, STDOUT
from typing import Optional, Callable
import time
import json

from loguru import logger


def set_logger(argv: list, logger: logger.__class__):
    if "-v" not in argv:
        logger.remove()
        logger.add(level="INFO", sink=sys.stderr)


@dataclass
class DiscoveryResult:
    name: str
    type: str
    version: str
    details: Optional[dict]

    def __str__(self) -> str:
        resulted_str = ""
        data = dict(version=self.version, name=self.name, type=self.type)

        resulted_str += "Discovered software:\n"
        for key, value in data.items():
            resulted_str += f" * {key:18} = {value}" + "\n"
        if self.details:
            resulted_str += "Details:\n"
            for detail, value in self.details.items():
                resulted_str += f" * {detail:18} = {value}" + "\n"

        return resulted_str


@dataclass
class Software(ABC):
    """
    This is a base abstract class - "Software" for creating "Pattern" subclasses.

    Pattern is class used to model some piece of software installed/running in the system,
    it is a subclass of Software (current class) which has some abstract methods required to be implemented:

    * get_type
        * Returns str - the type of discovered software
    * get_name
        * Returns str - the name/instance ID of discovered software
    * get_version
        * Returns str - the version of discovered software
    * get_details
        * Returns dict - the key-valued map of various optional additional details of the discovered software

    After new Pattern class has these methods implemented, it is possible to discover the software.
    The inherited discover method will automatically run those methods and print out the software detailed information.

    """

    emulated_delay: int = 0

    def run_cmd(self, cmd: str, encoding: str = "utf-8", delay=0) -> str:
        # Emulating delay
        if delay >= 0:
            time.sleep(delay)

        raw_result = check_output(cmd, stderr=STDOUT).decode(encoding).rstrip()
        logger.debug(f"Raw result of '{cmd}':" + "\n" + raw_result)
        return raw_result

    def get_file(
        self, filename: str, encoding: str = "utf-8", delay=0
    ) -> Optional[str]:
        # Emulating delay
        if delay >= 0:
            time.sleep(delay)

        result: str = ""
        try:
            with open(
                filename.replace("~", expanduser("~")), "r", encoding=encoding
            ) as f:
                result = f.read().rstrip()
                logger.debug(f"Raw content of file '{filename}':" + "\n" + result)
        except Exception as e:
            logger.error(
                f"Failed to read the file '{filename}' ({e.__class__.__name__}:{e})"
            )
        return result

    @abstractmethod
    def get_type(self):
        return ""

    @abstractmethod
    def get_version(self) -> Optional[str]:
        ...

    @abstractmethod
    def get_name(self) -> Optional[str]:
        ...

    @abstractmethod
    def get_details(self) -> Optional[dict]:
        ...

    @staticmethod
    def json(data: str) -> Optional[dict]:
        try:
            return json.loads(data)
        except Exception as e:
            logger.error(f"Failed to parse json: ({e.__class__.__name__}:{e})")
            return {}

    def discover(self) -> DiscoveryResult:
        return DiscoveryResult(
            name=self.get_name(),
            type=self.get_type(),
            version=self.get_version(),
            details=self.get_details(),
        )


@dataclass
class emulate_long_running:
    seconds: int = 3

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            time.sleep(self.seconds)
            return func(*args, **kwargs)

        return wrapper