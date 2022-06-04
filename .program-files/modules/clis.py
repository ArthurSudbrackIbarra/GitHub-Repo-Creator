from .parsers import YAMLParser
from .interpreters import YAMLInterpreter
from .tokens import TokenManager
from .apis import GitHubAPI
from .terminal_commands import CommandRunner


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
                    print("\nUser successfully authenticated.\n")
                return True
            return False
        except Exception as error:
            if logs:
                print(error)
            self.githubAPI = None
            return False

    # Template.
    def template(self, templateType: str) -> bool:
        print(f"Template: {templateType}")
        return True

    # Create.
    def create(self, absoluteFilePath: str) -> bool:
        if not self.isAuthenticated():
            print(
                "User not authenticated to GitHub, run 'grc authenticate <YOUR_ACCESS_TOKEN>' to authenticate.")
            return False
        parser = YAMLParser(absoluteFilePath)
        yaml = YAMLInterpreter(parser)
        repoName = yaml.repoName()
        repoDescription = yaml.repoDescription() or ""
        private = yaml.private()
        autoClone = yaml.autoClone()
        if repoName is None:
            print("Error. The repository name was not specified.")
            return False
        if private is None:
            private = True
        if autoClone is None:
            autoClone = True
        # Creating repository.
        try:
            self.githubAPI.createRepo(
                name=repoName,
                description=repoDescription,
                private=private
            )
        except Exception as error:
            print(error)
            return False
        # Cloning repository.
        if autoClone:
            try:
                cloneURL = self.githubAPI.getRepoCloneURL(repoName)
                runner = CommandRunner()
                runner.gitClone(cloneURL)
            except Exception as error:
                print(error)
        # Collaborators.
        collaboratorsCount = yaml.collaboratorsCount()
        for i in range(collaboratorsCount):
            collaboratorName = yaml.collaboratorName(i)
            collaboratorPermission = yaml.collaboratorPermission(i) or "admin"
            if collaboratorName is None:
                print(
                    f"No name specified for collaborator {i}, cannot add collaborator.")
            else:
                try:
                    self.githubAPI.addCollaborator(
                        repoName=repoName,
                        collaboratorName=collaboratorName,
                        permission=collaboratorPermission
                    )
                except Exception as error:
                    print(error)
        return True
