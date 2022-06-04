from os import system


class CommandRunner:
    def __init__(self) -> None:
        pass

    def gitClone(self, cloneURL: str) -> None:
        system(f"git clone {cloneURL}")
