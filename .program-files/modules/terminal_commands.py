from os import system


class CommandRunner:
    def __init__(self) -> None:
        pass

    def gitClone(self, cloneURL: str) -> int:
        print()
        return system(f"git clone {cloneURL}")
