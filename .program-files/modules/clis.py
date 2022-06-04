from os import path
from .parsers import YAMLParser
from .interpreters import YAMLInterpreter
from .tokens import TokenManager
from .apis import GitHubAPI
from .file_managers import FileCopier, FileChooser
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

    def authenticate(self, accessToken: str, logs: bool = False) -> bool:
        try:
            if len(accessToken) > 0:
                self.githubAPI = GitHubAPI(accessToken)
                self.tokenManager.writeToken(accessToken)
                if logs:
                    print(
                        f"\n{GREEN}[SUCCESS]{RESET} User authenticated.")
                return True
            return False
        except Exception as error:
            if logs:
                print(error)
            self.githubAPI = None
            return False

    # Save.
    def save(self, absoluteFilePath: str) -> bool:
        if not absoluteFilePath.endswith(".yaml"):
            print(
                f"\n{RED}[ERROR]{RESET} Only .yaml files can be saved to your templates.")
            return False
        copier = FileCopier(absoluteFilePath)
        templatesPath = path.abspath(
            path.join(path.dirname(__file__), "../../templates"))
        copier.copyTo(templatesPath)
        print(f"\n{GREEN}[SUCCESS]{RESET} File saved!")
        return True

    # Choose.
    def choose(self) -> None:
        templatesPath = path.abspath(
            path.join(path.dirname(__file__), "../../templates"))
        chooser = FileChooser(templatesPath)
        print("\n" + ("=" * 40))
        files = chooser.getFiles()
        for index, file in enumerate(files):
            print(f"{CYAN}[{index}]{RESET} - {file}")
        print("=" * 40)
        option = -1
        try:
            option = int(input("\nChoose which file to use: "))
        except:
            print(f"\n{RED}[ERROR]{RESET} Option must be a number.")
            return
        filePath = chooser.getFilePath(option)
        if filePath is None:
            print(f"\n{RED}[ERROR]{RESET} Invalid choice.")
            return
        print("\nWould you like to change the repository name and/or description?")
        print(f"\n{GREEN}[Y/y]{RESET} - Yes, I want to change.")
        print(
            f"{RED}[Other]{RESET} - No, keep the name/description from the template file.\n")
        change = input()
        if change == "Y" or change == "y":
            repoName = input("\nRepository name: ")
            repoDescription = input("Repository description: ")
            # Calling the create command with optional arguments.
            self.create(filePath, repoName=repoName,
                        repoDescription=repoDescription)
        else:
            # Calling the create command.
            self.create(filePath)

    # Create.
    def create(self, absoluteFilePath: str, repoName: str = None, repoDescription: str = None) -> bool:
        if not self.isAuthenticated():
            print(
                f"\nUser not authenticated to GitHub, run '{CYAN}grc{RESET} authenticate <YOUR_ACCESS_TOKEN>' to authenticate.")
            return False
        parser = YAMLParser(absoluteFilePath)
        yaml = YAMLInterpreter(parser)
        if repoName is None:
            repoName = yaml.repoName()
        if repoDescription is None:
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
            print(
                f"\n{GREEN}[SUCCESS]{RESET} Repository created with success!")
        except Exception as error:
            print(error)
            return False
        # Cloning repository.
        if autoClone:
            try:
                cloneURL = self.githubAPI.getRepoCloneURL(repoName)
                runner = CommandRunner()
                status = runner.gitClone(cloneURL)
                if status == 0:
                    print(
                        f"\n{GREEN}[SUCCESS]{RESET} Repository cloned with success!")
                else:
                    print(
                        f"\n{RED}[ERROR]{RESET} Unnable to clone repository.")
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
