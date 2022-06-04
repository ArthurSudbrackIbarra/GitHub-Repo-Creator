from os import system


class CommandRunner:
    def __init__(self) -> None:
        pass

    def gitClone(self, cloneURL: str) -> None:
        print()
        system(f"git clone {cloneURL}")
        print("\n")
