from os import path
from time import time


class VersionManager:
    def __init__(self, daysInCache: int) -> None:
        self.versionPath = path.abspath(
            path.join(path.dirname(__file__), '../config/VERSION'))
        self.daysInCache = daysInCache if daysInCache > 0 else 1

    # readVersion is not used...
    def readVersion(self) -> str:
        with open(self.versionPath, 'r') as versionFile:
            return versionFile.readline()

    def writeVersion(self, version: str) -> None:
        with open(self.versionPath, 'w') as versionFile:
            versionFile.write(version)

    def shouldResetCache(self) -> float:
        return (time() - path.getatime(self.versionPath)) >= 0
        return (time() - path.getatime(self.versionPath)) >= (86400 * self.daysInCache)
