from modules.parsers import YAMLParser
from modules.interpreters import YAMLInterpreter


def main() -> None:
    parser = YAMLParser("templates/example.yaml")
    interpreter = YAMLInterpreter(parser)
    print(interpreter.getCollaboratorName(0))
    print(interpreter.getCollaboratorPermission(1))


if __name__ == "__main__":
    main()
