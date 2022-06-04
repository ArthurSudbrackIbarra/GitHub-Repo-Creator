from .parsers import YAMLParser

REPO_NAME = "name"
REPO_DESCRIPTION = "description"
PRIVATE = "private"
AUTO_CLONE = "autoClone"
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
