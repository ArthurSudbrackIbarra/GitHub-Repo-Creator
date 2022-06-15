from os import system
from os.path import exists
from sys import platform
from subprocess import check_output


class CommandRunner:
    @staticmethod
    def gitClone(cloneURL: str) -> int:
        print("")
        return system(f"git clone {cloneURL}")

    @staticmethod
    def gitLocalToRemote(repoURL: str) -> int:
        print("")
        exitCode = system("git init")
        if exitCode != 0:
            return exitCode
        exitCode = system("git branch -M main")
        if exitCode != 0:
            return exitCode
        exitCode = system(f"git remote add origin {repoURL}")
        if exitCode != 0:
            return exitCode
        exitCode = system("git add .")
        if exitCode != 0:
            return exitCode
        exitCode = system(
            "git commit -m \"Automatic Commit using GRC (https://github.com/ArthurSudbrackIbarra/GitHub-Repo-Creator).\"")
        if exitCode != 0:
            return exitCode
        return system("git push -u origin main")

    @staticmethod
    def openTextEditor(absoluteFilePath: str) -> int:
        if absoluteFilePath is None or not exists(absoluteFilePath):
            return 1
        # First tries to open the file with VSCode.
        # If the user does not have VSCode installed, then uses native text editors.
        exitCode = system(f"code {absoluteFilePath}")
        if exitCode != 0:
            if platform.startswith("win"):
                return system(f"notepad {absoluteFilePath}")
            elif platform.startswith("linux") or platform.startswith("darwin"):
                return system(f"nano {absoluteFilePath}")
            return 1
        return exitCode

    @staticmethod
    def getGRCCurrentVersion(repoPath: str) -> str:
        shell = True if platform.startswith("win") else False
        try:
            outputAsBytes = check_output(
                ["git", "--git-dir", f"{repoPath}/.git", "describe", "--tags"], shell=shell)
            output = outputAsBytes.decode()
            return output.strip().split("-")[0]
        except:
            return None

    @staticmethod
    def updateGRCVersion(repoPath: str, latestTag: str) -> int:
        gitDirFlag = f"--git-dir {repoPath}/.git"
        exitCode = system(f"git {gitDirFlag} fetch --tags --quiet")
        if exitCode != 0:
            return exitCode
        return system(f"git {gitDirFlag} checkout -f tags/{latestTag} --quiet")

    @staticmethod
    def getUserCurrentDir() -> str:
        shell = True if platform.startswith("win") else False
        command = "cd" if shell else "pwd"
        try:
            outputAsBytes = check_output(
                [command], shell=shell)
            output = outputAsBytes.decode()
            return output.strip()
        except:
            return None
