from .parsers import YAMLParser
from .interpreters import YAMLInterpreter
from .tokens import TokenManager
from .apis import GitHubAPI
from .terminal_commands import CommandRunner
from .coloring import Colors

GREEN = Colors.GREEN
YELLOW = Colors.YELLOW
RED = Colors.RED
CYAN = Colors.CYAN
RESET = Colors.RESET


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
                    print(
                        f"\n{GREEN}[SUCCESS]{RESET} User authenticated.\n")
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
                f"\nUser not authenticated to GitHub, run '{CYAN}grc{RESET} authenticate <YOUR_ACCESS_TOKEN>' to authenticate.\n")
            return False
        parser = YAMLParser(absoluteFilePath)
        yaml = YAMLInterpreter(parser)
        repoName = yaml.repoName()
        repoDescription = yaml.repoDescription() or ""
        private = yaml.private()
        autoClone = yaml.autoClone()
        if repoName is None:
            print(
                f"\n{RED}[ERROR]{RESET}. The repository name was not specified.")
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
                    f"\n{YELLOW}[WARN]{RESET} No name specified for collaborator {i}, cannot add collaborator.")
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
