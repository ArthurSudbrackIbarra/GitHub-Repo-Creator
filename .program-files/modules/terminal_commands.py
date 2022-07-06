from os import system
from os.path import exists
from sys import platform
from subprocess import check_output


class CommandRunner:
    @staticmethod
    def gitClone(repoName: str, accessToken: str, username: str) -> int:
        print("")
        cloneURL = f"https://{accessToken}@github.com/{username}/{repoName}.git"
        return system(f"git clone {cloneURL}")

    @staticmethod
    def code(repoPath: str) -> int:
        return system(f"code \"{repoPath}\"")

    @staticmethod
    def gitLocalToRemote(repoName: str, accessToken: str, username: str) -> int:
        print("")
        exitCode = system("git init")
        if exitCode != 0:
            return exitCode
        exitCode = system("git branch -M main")
        if exitCode != 0:
            return exitCode
        originURL = f"https://{username}:{accessToken}@github.com/{username}/{repoName}.git"
        exitCode = system(
            f"git remote add origin {originURL}")
        if exitCode != 0:
            return exitCode
        exitCode = system("git add .")
        if exitCode != 0:
            return exitCode
        exitCode = system(
            "git commit -m \"Automatic Commit using GRC.\"")
        if exitCode != 0:
            return exitCode
        return system("git push -u origin main")

    @staticmethod
    def openFileInTextEditor(absoluteFilePath: str) -> int:
        if absoluteFilePath is None or not exists(absoluteFilePath):
            return 1
        # First tries to open the file with VSCode.
        # If the user does not have VSCode installed, then uses native text
        # editors.
        exitCode = system(f"code \"{absoluteFilePath}\"")
        if exitCode != 0:
            if platform.startswith("win"):
                return system(f"notepad \"{absoluteFilePath}\"")
            elif platform.startswith("linux") or platform.startswith("darwin"):
                return system(f"nano \"{absoluteFilePath}\"")
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
        except BaseException:
            return None

    @staticmethod
    def updateGRCVersion(repoPath: str, latestTag: str) -> int:
        gitDirFlag = f"--git-dir \"{repoPath}/.git\""
        exitCode = system(f"git {gitDirFlag} checkout --force main --quiet")
        if exitCode != 0:
            return exitCode
        exitCode = system(f"git {gitDirFlag} pull --quiet")
        if exitCode != 0:
            return exitCode
        return system(
            f"git {gitDirFlag} checkout --force tags/{latestTag} --quiet")
