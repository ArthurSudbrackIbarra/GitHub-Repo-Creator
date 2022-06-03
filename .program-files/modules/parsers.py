from os import path
from typing import Any
import yaml
from yaml.loader import SafeLoader


class YAMLParser:
    def __init__(self, filePath: str) -> None:
        self.absoluteFilePath = path.abspath(filePath)

    def load(self) -> Any:
        with open(self.absoluteFilePath) as yamlFile:
            data = yaml.load(yamlFile, Loader=SafeLoader)
            return data
