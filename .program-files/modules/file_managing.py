from os import path, listdir, scandir, DirEntry, remove, unlink
from shutil import copy, rmtree


class FileCopier:
    def __init__(self, filePath: str) -> None:
        self.absoluteFilePath = path.abspath(filePath)

    def copyTo(self, copyPath: str) -> None:
        copy(self.absoluteFilePath, copyPath)


class FileChooser:
    def __init__(self, dirPath: str) -> None:
        self.absoluteDirPath = path.abspath(dirPath)

    def getFileNames(self, fileExtension: str = ".yaml") -> "list[str]":
        files = [
            file for file in listdir(
                self.absoluteDirPath) if path.isfile(
                path.join(
                    self.absoluteDirPath,
                    file)) and file.endswith(fileExtension)]
        return files

    def getFilesInfo(
            self,
            fileExtension: str = ".yaml") -> "list[DirEntry[str]]":
        files = [
            file for file in scandir(
                self.absoluteDirPath) if path.isfile(
                path.join(
                    self.absoluteDirPath,
                    file)) and file.name.endswith(fileExtension)]
        return files

    def getFilePathByIndex(
            self,
            index: int,
            fileExtension: str = ".yaml") -> str:
        files = self.getFileNames(fileExtension)
        if len(files) >= index + 1:
            return path.join(self.absoluteDirPath, files[index])
        return None

    def getFilePathByName(self, name: str) -> str:
        files = self.getFilesInfo(fileExtension="")
        for file in files:
            if file.name == name:
                return file.path
        return None

    def getFileContentByName(self, name: str) -> str:
        files = self.getFilesInfo(fileExtension="")
        for file in files:
            if file.name == name:
                with open(file.path, 'r') as template:
                    return template.read()
        return None


class FileDeleter:
    @staticmethod
    def deleteFile(absoluteFilePath) -> bool:
        try:
            remove(absoluteFilePath)
            return True
        except BaseException:
            return False

    @staticmethod
    def deleteAllFromFolder(absoluteDirPath) -> None:
        for filename in listdir(absoluteDirPath):
            filePath = path.join(absoluteDirPath, filename)
            try:
                if path.isfile(filePath) or path.islink(filePath):
                    unlink(filePath)
                elif path.isdir(filePath):
                    rmtree(filePath)
            except BaseException:
                pass
