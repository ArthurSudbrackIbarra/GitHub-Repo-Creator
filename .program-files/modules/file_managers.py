from os import path, listdir, remove, unlink
import shutil


class FileCopier:
    def __init__(self, filePath: str) -> None:
        self.absoluteFilePath = path.abspath(filePath)

    def copyTo(self, copyPath: str) -> None:
        shutil.copy(self.absoluteFilePath, copyPath)


class FileChooser:
    def __init__(self, dirPath: str) -> None:
        self.absoluteDirPath = path.abspath(dirPath)

    def getFiles(self, fileExtension: str = ".yaml") -> None:
        files = [file for file in listdir(self.absoluteDirPath) if path.isfile(
            path.join(self.absoluteDirPath, file)) and file.endswith(fileExtension)]
        return files

    def getFilePath(self, index: int, fileExtension: str = ".yaml") -> str:
        files = self.getFiles(fileExtension)
        if len(files) >= index + 1:
            return path.join(self.absoluteDirPath, files[index])
        return None


class FileDeleter:
    @staticmethod
    def deleteFile(absoluteFilePath) -> bool:
        try:
            remove(absoluteFilePath)
            return True
        except:
            return False

    @staticmethod
    def deleteAllFromFolder(absoluteDirPath) -> None:
        for filename in listdir(absoluteDirPath):
            filePath = path.join(absoluteDirPath, filename)
            try:
                if path.isfile(filePath) or path.islink(filePath):
                    unlink(filePath)
                elif path.isdir(filePath):
                    shutil.rmtree(filePath)
            except:
                pass
