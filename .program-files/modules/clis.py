from .parsers import YAMLParser
from .interpreters import YAMLInterpreter
from .tokens import TokenManager
from .apis import GitHubAPI


class CLI:
    def __init__(self) -> None:
        self.tokenManager = TokenManager()
        self.githubAPI = None

    def isAuthenticated(self) -> bool:
        return self.githubAPI is not None

    # Take a look into this method.
    def authenticate(self, accessToken: str, logs: bool = False) -> bool:
        try:
            if len(accessToken) > 0:
                self.githubAPI = GitHubAPI(accessToken)
                self.tokenManager.writeToken(accessToken)
                if logs:
                    print("\n[User successfully authenticated]\n")
            return False
        except Exception as error:
            print(error)
            return False

    # Template.
    def template(self, templateType: str) -> bool:
        print(f"Template: {templateType}")
        return True

    # Create.
    def create(self, absoluteFilePath: str) -> bool:
        print(f"Create: {absoluteFilePath}")
        if not self.isAuthenticated():
            print(
                "User not authenticated to GitHub, run 'grc authenticate <YOUR_ACCESS_TOKEN>' to authenticate.")
            return False
        # Refactor this later...
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
