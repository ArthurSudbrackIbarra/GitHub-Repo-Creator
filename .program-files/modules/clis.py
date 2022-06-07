from fileinput import filename
from os import path
from .parsers import YAMLParser
from .interpreters import YAMLInterpreter
from .tokens import TokenManager
from .apis import GitHubAPI
from .file_managers import FileCopier, FileChooser, FileDeleter
from .terminal_commands import CommandRunner
from .coloring import Colors

GREEN = Colors.GREEN
YELLOW = Colors.YELLOW
RED = Colors.RED
CYAN = Colors.CYAN
BLUE = Colors.BLUE
RESET = Colors.RESET


class CLI:
    def __init__(self) -> None:
        self.tokenManager = TokenManager()
        self.githubAPI = None

    # Authenticate.
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
        self.list(enumeration=True)
        option = -1
        try:
            option = int(input("\nChoose which file to use: "))
        except:
            print(f"\n{RED}[ERROR]{RESET} Option must be a number.")
            return
        templatesPath = path.abspath(
            path.join(path.dirname(__file__), "../../templates"))
        chooser = FileChooser(templatesPath)
        filePath = chooser.getFilePathByIndex(option)
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
    def create(self,
               absoluteFilePath: str,
               repoName: str = None,
               repoDescription: str = None) -> bool:
        if self.githubAPI is None or not self.githubAPI.isAuthenticated():
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
        autoPush = yaml.autoPush()
        if repoName is None:
            print(
                f"\n{RED}[ERROR]{RESET}. The repository name was not specified.")
            return False
        if private is None:
            private = True
        if autoClone is None:
            autoClone = False
        if autoPush is None or (autoPush == True and autoClone == True):
            autoPush = False
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
                exitCode = CommandRunner.gitClone(cloneURL)
                if exitCode == 0:
                    print(
                        f"\n{GREEN}[SUCCESS]{RESET} Repository cloned with success!")
                else:
                    print(
                        f"\n{RED}[ERROR]{RESET} Unnable to clone repository.")
            except Exception as error:
                print(error)
        # Pushing content.
        if autoPush and not autoClone:
            try:
                cloneURL = self.githubAPI.getRepoCloneURL(repoName)
                exitCode = CommandRunner.gitLocalToRemote(
                    cloneURL, "Initial Commit.")
                if exitCode == 0:
                    print(
                        f"\n{GREEN}[SUCCESS]{RESET} Pushed content to repository with success!")
                else:
                    print(
                        f"\n{RED}[ERROR]{RESET} Unnable to push content to repository.")
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

    # List.
    def list(self, enumeration: bool = False) -> None:
        templatesPath = path.abspath(
            path.join(path.dirname(__file__), "../../templates"))
        chooser = FileChooser(templatesPath)
        fileNames = chooser.getFileNames()
        if len(fileNames) <= 0:
            print(
                f"No files to list, create templates by running '{CYAN}grc{RESET} save <PATH_TO_YOUR_YAML>'.")
            return
        print("")
        for index, fileName in enumerate(fileNames):
            if enumeration:
                print(f"{CYAN}[{index}]{RESET} - {fileName}")
            else:
                print(fileName)

    # Get.
    def get(self, templateName: str) -> bool:
        templatesPath = path.abspath(
            path.join(path.dirname(__file__), "../../templates"))
        chooser = FileChooser(templatesPath)
        if not templateName.endswith(".yaml"):
            templateName += ".yaml"
        content = chooser.getFileContentByName(templateName)
        if content is None:
            print(
                f"\n{RED}[ERROR]{RESET} Template '{templateName}' not found.")
            return False
        print(f"\n{content}")
        return True

    # Edit.
    def edit(self, templateName: str) -> bool:
        templatesPath = path.abspath(
            path.join(path.dirname(__file__), "../../templates"))
        chooser = FileChooser(templatesPath)
        if not templateName.endswith(".yaml"):
            templateName += ".yaml"
        filePath = chooser.getFilePathByName(templateName)
        exitCode = CommandRunner.openTextEditor(filePath)
        if exitCode == 0:
            return True
        print(
            f"\n{RED}[ERROR]{RESET} Unnable to edit template, make sure the file exists.")
        return False

    # Delete.
    def delete(self, templateName: str) -> bool:
        if templateName == "all":
            dirPath = path.abspath(
                path.join(path.dirname(__file__), "../../templates"))
            FileDeleter.deleteAllFromFolder(dirPath)
            print(
                f"\n{GREEN}[SUCCESS]{RESET} Templates cleared!")
            return True
        else:
            if not templateName.endswith(".yaml"):
                templateName += ".yaml"
            filePath = path.abspath(
                path.join(path.dirname(__file__), f"../../templates/{templateName}"))
            deleted = FileDeleter.deleteFile(filePath)
            if deleted:
                print(
                    f"\n{GREEN}[SUCCESS]{RESET} Template deleted with success!")
                return True
            print(
                f"\n{RED}[ERROR]{RESET} Unnable to delete template, make sure the file exists.")
            return False

    # Version.
    def version(self, repoPath: str) -> bool:
        if self.githubAPI is None or not self.githubAPI.isAuthenticated():
            print(
                f"\nUser not authenticated to GitHub, run '{CYAN}grc{RESET} authenticate <YOUR_ACCESS_TOKEN>' to authenticate.\n")
            return False
        version = CommandRunner.getGRCCurrentVersion(repoPath)
        if version is None:
            print(
                f"\n{RED}[ERROR]{RESET} Unnable to get GRC current version.")
            return False
        print(f"\nGRC version {version}\n")
        return True

    # Helper method.
    def isLatestVersion(self, version: str) -> "list":
        try:
            latestTag = self.githubAPI.getGRCLatestTag()
            if not version.startswith(latestTag):
                return [False, latestTag]
            return [True, latestTag]
        except Exception as error:
            print(error)
            return [False, latestTag]

    # Update.
    def update(self, repoPath: str) -> bool:
        if self.githubAPI is None or not self.githubAPI.isAuthenticated():
            print(
                f"\nUser not authenticated to GitHub, run '{CYAN}grc{RESET} authenticate <YOUR_ACCESS_TOKEN>' to authenticate.")
            return False
        currentVersion = CommandRunner.getGRCCurrentVersion(repoPath)
        if currentVersion is None:
            print(
                f"\n{RED}[ERROR]{RESET} Unnable to get GRC current version.")
            return False
        latestVersionInfo = self.isLatestVersion(currentVersion)
        isLatestVersion = latestVersionInfo[0]
        latestTag = latestVersionInfo[1]
        if not isLatestVersion:
            exitCode = CommandRunner.updateGRCVersion(repoPath, latestTag)
            if exitCode == 0:
                print(
                    f"\n{GREEN}[SUCCESS]{RESET} GRC updated to latest version!")
                return True
            print(
                f"\n{RED}[ERROR]{RESET} Unnable to update GRC to latest version.")
        print("\nAlready using GRC latest version.")
        return False

    # Help
    def help(self) -> None:
        print(
            "\nWhat is GRC?\nGRC is a tool to automatically create GitHub repositories using YAML templates.")
        print(
            "\n[COMMANDS]")
        print(
            f"\n{BLUE}help{RESET}\n\nShows this message.")
        print(
            f"\n{BLUE}authenticate{RESET} {CYAN}<ACCESS_TOKEN>{RESET}\n\nAuthenticates to GitHub in order to create repositories in your account.")
        print(
            f"\n{BLUE}create{RESET} {CYAN}<PATH_TO_YOUR_YAML_FILE>{RESET}\n\nCreates a repository for you based on a YAML file that is passed as a parameter.")
        print(
            f"\n{BLUE}save{RESET} {CYAN}<PATH_TO_YOUR_YAML_FILE>{RESET}\n\nSaves a YAML file to your templates, so that you can later use it to create another repository with the same configurations.")
        print(
            f"\n{BLUE}list{RESET}\n\nLists all the templates that are saved in your machine.")
        print(
            f"\n{BLUE}get{RESET} {CYAN}<TEMPLATE_NAME>{RESET}\n\nThe 'get' command shows the content of a template that is saved in your machine.")
        print(
            f"\n{BLUE}choose{RESET}\n\nLets you choose a file from your saved templates to create a repository based on it.")
        print(
            f"\n{BLUE}edit{RESET} {CYAN}<TEMPLATE_NAME>{RESET}\n\nOpens a text editor and lets you edit one of your saved templates.")
        print(
            f"\n{BLUE}delete{RESET} {CYAN}<TEMPLATE_NAME>{RESET}\n\nDeletes a template from your saved templates.")
        print(
            f"\n{BLUE}version{RESET}\n\nShows you the GRC version that you are currently using.")
        print(
            f"\n{BLUE}update{RESET}\n\nAutomatically installs the latest GRC version in case you're still not using it.\n")
