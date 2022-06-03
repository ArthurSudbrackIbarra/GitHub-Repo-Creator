import click
from .parsers import YAMLParser
from .interpreters import YAMLInterpreter
from .apis import GitHubAPI


class CLI:
    def __init__(self) -> None:
        self.githubAPI = None

    # Authenticate.
    def authenticate(self, accessToken: str) -> bool:
        try:
            self.githubAPI = GitHubAPI(accessToken)
        except Exception as error:
            print(error)
            raise Exception("Error when trying to authenticate to GitHub.")

    # Set token.
    def setToken(self, accessToken: str) -> bool:
        print(f"Setar token: {accessToken}")

    # Template.
    def template(self, templateType: str) -> bool:
        print(f"Template: {templateType}")

    # Create.
    def create(self, absoluteFilePath: str) -> bool:
        print(f"Criar: {absoluteFilePath}")
        exit(0)
        # Para depois...
        parser = YAMLParser(absoluteFilePath)
        interpreter = YAMLInterpreter(parser)
        repoName = interpreter.getRepoName()
        repoDescription = interpreter.getRepoDescription()
        private = interpreter.getPrivate()
        if not (repoName is None or repoDescription is None or private is None):
            self.githubAPI.createRepo(
                name=repoName,
                description=repoDescription,
                private=private
            )
            collaboratorsCount = interpreter.getCollaboratorsCount()
            for i in range(collaboratorsCount):
                collaboratorName = interpreter.getCollaboratorName(i)
                collaboratorPermission = interpreter.getCollaboratorPermission(
                    i)
                if not (collaboratorName is None or collaboratorPermission is None):
                    self.githubAPI.addCollaborator(
                        repoName=repoName,
                        collaboratorName=collaboratorName,
                        permission=collaboratorPermission
                    )
