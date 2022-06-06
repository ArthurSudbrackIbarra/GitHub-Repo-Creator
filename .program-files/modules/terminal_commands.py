from os import system
from sys import platform


class CommandRunner:
    @staticmethod
    def gitClone(cloneURL: str) -> int:
        print("")
        return system(f"git clone {cloneURL}")

    @staticmethod
    def gitLocalToRemote(repoURL: str, commitMessage: str) -> int:
        print("")
        exitCode = system("git init --initial-branch=main")
        if exitCode != 0:
            return exitCode
        exitCode = system(f"git remote add origin {repoURL}")
        if exitCode != 0:
            return exitCode
        exitCode = system("git fetch")
        if exitCode != 0:
            return exitCode
        exitCode = system("git pull origin main")
        if exitCode != 0:
            return exitCode
        exitCode = system("git add .")
        if exitCode != 0:
            return exitCode
        exitCode = system(f"git commit -m \"{commitMessage}\"")
        if exitCode != 0:
            return exitCode
        return system("git push --all origin")

    @staticmethod
    def openTextEditor(absoluteFilePath: str) -> int:
        if platform.startswith("win"):
            return system(f"notepad {absoluteFilePath}")
        elif platform.startswith("linux") or platform.startswith("darwin"):
            return system(f"nano {absoluteFilePath}")
        return 1
