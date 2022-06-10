from sys import platform, stdout
from os import environ


def terminalSupportsColor():
    def vtCodesEnabledInWindowsRegistry():
        try:
            import winreg
        except ImportError:
            return False
        else:
            try:
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Console")
                reg_key_value, _ = winreg.QueryValueEx(
                    reg_key, "VirtualTerminalLevel")
            except FileNotFoundError:
                return False
            else:
                return reg_key_value == 1
    is_a_tty = hasattr(stdout, "isatty") and stdout.isatty()
    return is_a_tty and (
        platform != "win32" or "ANSICON" in environ or "WT_SESSION" in environ or environ.get(
            "TERM_PROGRAM") == "vscode" or vtCodesEnabledInWindowsRegistry()
    )


supportsColor = terminalSupportsColor()


class Colors:
    HEADER = ""
    BLUE = ""
    CYAN = ""
    GREEN = ""
    YELLOW = ""
    RED = ""
    RESET = ""
    BOLD = ""
    UNDERLINE = '\033[4m'
    if supportsColor:
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        print("Entrou aqui!")
