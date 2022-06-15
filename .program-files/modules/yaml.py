from os import path
from typing import Any
import yaml
from yaml.loader import SafeLoader


class YAMLParser:
    def __init__(self, filePath: str) -> None:
        self.absoluteFilePath = path.abspath(filePath)

    def load(self) -> Any:
        with open(self.absoluteFilePath, 'r') as yamlFile:
            data = yaml.load(yamlFile, Loader=SafeLoader)
            return data


REPO_NAME = "name"
REPO_PATH = "path"
REPO_DESCRIPTION = "description"
PRIVATE = "private"

# For retrocompatibility.
AUTO_CLONE = "autoClone"
AUTO_PUSH = "autoPush"

# New version of autoClone and autoPush.
INCLUDE_CONTENT = "includeContent"

COLLABORATORS = "collaborators"
COLLABORATOR = "collaborator"
COLLABORATOR_NAME = "name"
COLLABORATOR_PERMISSION = "permission"


class YAMLInterpreter:
    def __init__(self, parser: YAMLParser) -> None:
        self.data = parser.load()

    def repoName(self) -> str:
        if REPO_NAME in self.data:
            return self.data[REPO_NAME]
        return None

    def repoPath(self) -> str:
        if REPO_PATH in self.data:
            return self.data[REPO_PATH]
        return None

    def repoDescription(self) -> str:
        if REPO_DESCRIPTION in self.data:
            return self.data[REPO_DESCRIPTION]
        return None

    def private(self) -> bool:
        if PRIVATE in self.data:
            return self.data[PRIVATE]
        return None

    def autoClone(self) -> bool:
        if AUTO_CLONE in self.data:
            return self.data[AUTO_CLONE]
        return None

    def autoPush(self) -> bool:
        if AUTO_PUSH in self.data:
            return self.data[AUTO_PUSH]
        return None

    def includeContent(self) -> bool:
        if INCLUDE_CONTENT in self.data:
            return self.data[INCLUDE_CONTENT]
        return None

    def collaboratorsCount(self) -> int:
        if COLLABORATORS in self.data:
            return len(self.data[COLLABORATORS])
        return 0

    def collaboratorName(self, index: int) -> str:
        if COLLABORATORS in self.data:
            collaborators = self.data[COLLABORATORS]
            if len(collaborators) >= index + 1:
                if COLLABORATOR in collaborators[index]:
                    collaborator = collaborators[index][COLLABORATOR]
                    if COLLABORATOR_NAME in collaborator:
                        return collaborator[COLLABORATOR_NAME]
                    return None
                return None
            return None

    def collaboratorPermission(self, index: int) -> str:
        if COLLABORATORS in self.data:
            collaborators = self.data[COLLABORATORS]
            if len(collaborators) >= index + 1:
                if COLLABORATOR in collaborators[index]:
                    collaborator = collaborators[index][COLLABORATOR]
                    if COLLABORATOR_PERMISSION in collaborator:
                        return collaborator[COLLABORATOR_PERMISSION]
                    return None
                return None
            return None


class YAMLWriter:
    def __init__(self, dirPath: str) -> None:
        self.absoluteDirPath = path.abspath(dirPath)

    def writeTemplate(self,
                      templateName: str,
                      repoName: str,
                      repoDescription: str,
                      private: bool,
                      includeContent: bool,
                      collaborators: "list[dict]") -> bool:
        data = {}
        data[REPO_NAME] = repoName
        data[REPO_DESCRIPTION] = repoDescription
        data[PRIVATE] = private
        data[INCLUDE_CONTENT] = includeContent
        if len(collaborators) > 0:
            data[COLLABORATORS] = []
        for collaborator in collaborators:
            data[COLLABORATORS].append(
                {COLLABORATOR: {COLLABORATOR_NAME: collaborator["name"], COLLABORATOR_PERMISSION: collaborator["permission"]}})
        with open(f"{self.absoluteDirPath}/{templateName}", "w+") as yamlFile:
            try:
                yaml.dump(data, yamlFile)
                return True
            except:
                return False

    def writeRepo(self,
                  templateName: str,
                  repoName: str,
                  repoPath: str) -> bool:
        data = {}
        data[REPO_NAME] = repoName
        data[REPO_PATH] = repoPath
        with open(f"{self.absoluteDirPath}/{templateName}", "w+") as yamlFile:
            try:
                yaml.dump(data, yamlFile)
                return True
            except:
                return False
