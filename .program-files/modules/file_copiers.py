from os import path
import shutil


class FileCopier:
    def __init__(self, filePath: str) -> None:
        self.absoluteFilePath = path.abspath(filePath)

    def copyTo(self, copyPath: str) -> None:
        shutil.copy(self.absoluteFilePath, copyPath)
