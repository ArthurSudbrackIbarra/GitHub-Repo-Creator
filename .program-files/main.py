from modules.parsers import YAMLParser
from modules.interpreters import YAMLInterpreter
from modules.apis import GitHubAPI


def main() -> None:
    parser = YAMLParser("templates/example.yaml")
    interpreter = YAMLInterpreter(parser)
    api = GitHubAPI("ACCESS_TOKEN")

    repoName = interpreter.getRepoName()
    repoDescription = interpreter.getRepoDescription()
    private = interpreter.getPrivate()

    if not (repoName is None or repoDescription is None or private is None):
        api.createRepo(
            name=repoName,
            description=repoDescription,
            private=private
        )

        collaboratorsCount = interpreter.getCollaboratorsCount()
        for i in range(collaboratorsCount):
            collaboratorName = interpreter.getCollaboratorName(i)
            collaboratorPermission = interpreter.getCollaboratorPermission(i)
            if not (collaboratorName is None or collaboratorPermission is None):
                api.addCollaborator(
                    repoName=repoName,
                    collaboratorName=collaboratorName,
                    permission=collaboratorPermission
                )


if __name__ == "__main__":
    main()
