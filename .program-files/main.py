from modules.parsers import YAMLParser
from modules.interpreters import YAMLInterpreter
from modules.apis import GitHubAPI


def main() -> None:
    parser = YAMLParser("templates/example.yaml")
    interpreter = YAMLInterpreter(parser)
    api = GitHubAPI("access token here")

    repoName = interpreter.getRepoName()
    repoDescription = interpreter.getRepoDescription()
    private = interpreter.getPrivate()

    if not (repoName is None or repoDescription is None or private is None):
        api.createRepo(
            name=repoName,
            description=repoDescription,
            private=private
        )


if __name__ == "__main__":
    main()
