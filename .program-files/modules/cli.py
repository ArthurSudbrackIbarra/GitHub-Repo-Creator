from os import path, getcwd
from re import sub
from .yaml import YAMLParser, YAMLInterpreter, YAMLWriter
from .token import TokenManager
from .api import GitHubAPI
from .file_managing import FileCopier, FileChooser, FileDeleter
from .terminal_commands import CommandRunner
from .coloring import Colors

GREEN = Colors.GREEN
YELLOW = Colors.YELLOW
RED = Colors.RED
CYAN = Colors.CYAN
BLUE = Colors.BLUE
HEADER = Colors.HEADER
RESET = Colors.RESET

TEMPLATES_PATH = path.abspath(
    path.join(path.dirname(__file__), "../../templates"))
REPOSITORIES_PATH = path.abspath(
    path.join(path.dirname(__file__), "../../repositories"))

TEMPLATE_NAME_PATTERN = r"[^a-zA-Z0-9-_]"
REPOSITORY_NAME_PATTERN = r"[^a-zA-Z0-9-._]"


# Absolute paths are not modified.
# Relative paths are modified to be absolute paths.
def handleFilePath(filePath: str) -> str:
    if path.isabs(filePath):
        return filePath
    return path.abspath(path.join(getcwd(), filePath))


# Helper function to create repository yaml files.
def createRepoFile(repoPath: str, repoName: str = None) -> None:
    repoPath = repoPath.replace("\\", "/")
    if repoName is None:
        repoName = repoPath.split("/")[-1]
    fileName = f"{repoName}.yaml"
    writer = YAMLWriter(REPOSITORIES_PATH)
    writer.writeRepo(
        fileName=fileName,
        repoName=repoName,
        repoPath=repoPath
    )


# Helper function, checks if the user is using GRC latest version and
# returns it.
def checkIfLatestVersion(version: str) -> "list":
    try:
        latestTag = GitHubAPI.getGRCLatestTag()
        if not version.startswith("v"):
            version = f"v{version}"
        if not version.startswith(latestTag):
            return [False, latestTag]
        return [True, latestTag]
    except Exception as error:
        print(error)
        return [False, latestTag]


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
    def save(self, filePath: str) -> bool:
        if not filePath.endswith(".yaml"):
            print(
                f"\n{RED}[ERROR]{RESET} Only .yaml files can be saved to your templates.")
            return False
        filePath = handleFilePath(filePath)
        copier = FileCopier(filePath)
        copier.copyTo(TEMPLATES_PATH)
        print(f"\n{GREEN}[SUCCESS]{RESET} File saved!")
        return True

    # Choose.
    def choose(
            self,
            templateName: str = None,
            private: bool = None,
            includeContent: bool = None) -> bool:
        if self.githubAPI is None or not self.githubAPI.isAuthenticated():
            print(
                f"\nUser not authenticated to GitHub, run '{CYAN}grc{RESET} authenticate <YOUR_ACCESS_TOKEN>' to authenticate.")
            return False
        chooser = FileChooser(TEMPLATES_PATH)
        filePath = ""
        if templateName is None:
            self.list(enumeration=True)
            option = -1
            try:
                option = int(input("\nChoose which file to use: "))
            except BaseException:
                print(f"\n{RED}[ERROR]{RESET} Option must be a number.")
                return False
            filePath = chooser.getFilePathByIndex(option)
            if filePath is None:
                print(f"\n{RED}[ERROR]{RESET} Invalid choice.")
                return False
        else:
            if not templateName.endswith(".yaml"):
                templateName += ".yaml"
            filePath = chooser.getFilePathByName(templateName)
            if filePath is None:
                print(
                    f"\n{RED}[ERROR]{RESET} Template '{templateName}' not found.")
                return False
        print("\nWould you like to change the repository name and/or description?")
        print(f"\n{GREEN}[Y/y]{RESET} - Yes, I want to change.")
        print(
            f"{RED}[Other]{RESET} - No, keep the name/description from the template file.\n")
        change = input()
        if change == "Y" or change == "y":
            repoName = input("\nRepository name: ")
            repoDescription = input("Repository description: ")
            # Calling the create command with optional arguments.
            return self.apply(
                filePath,
                repoName=repoName,
                repoDescription=repoDescription,
                private=private,
                includeContent=includeContent)
        else:
            # Calling the create command.
            return self.apply(
                filePath,
                private=private,
                includeContent=includeContent)

    # Apply.
    def apply(self,
              filePath: str,
              repoName: str = None,
              repoDescription: str = None,
              private: bool = None,
              includeContent: bool = None) -> bool:
        if self.githubAPI is None or not self.githubAPI.isAuthenticated():
            print(
                f"\nUser not authenticated to GitHub, run '{CYAN}grc{RESET} authenticate <YOUR_ACCESS_TOKEN>' to authenticate.")
            return False
        filePath = handleFilePath(filePath)
        if not path.exists(filePath):
            print(
                f"\n{RED}[ERROR]{RESET} The path you specified does not exist.")
            return False
        parser = YAMLParser(filePath)
        yaml = YAMLInterpreter(parser)
        if repoName is None:
            repoName = yaml.repoName()
        if repoName is None:
            print(
                f"\n{RED}[ERROR]{RESET}. The repository name was not specified.")
            return False
        repoName = sub(REPOSITORY_NAME_PATTERN, "-", repoName)
        if repoDescription is None:
            repoDescription = yaml.repoDescription() or ""
        if private is None:
            private = yaml.private()
        if private is None:
            private = True
        if includeContent is None:
            includeContent = yaml.includeContent()
        if includeContent is None:
            includeContent = False
        # Creating repository.
        try:
            createREADME = not includeContent
            self.githubAPI.createRepo(
                name=repoName,
                description=repoDescription,
                private=private,
                createREADME=createREADME
            )
            print(
                f"\n{GREEN}[SUCCESS]{RESET} Repository created with success!")
        except Exception as error:
            print(error)
            return False
        # Cloning repository.
        if not includeContent:
            try:
                cloneURL = self.githubAPI.getRepoCloneURL(repoName)
                exitCode = CommandRunner.gitClone(cloneURL)
                if exitCode == 0:
                    print(
                        f"\n{GREEN}[SUCCESS]{RESET} Repository cloned with success!")
                    createRepoFile(repoPath=f"{getcwd()}/{repoName}")
                else:
                    print(
                        f"\n{RED}[ERROR]{RESET} Unnable to clone repository.")
            except Exception as error:
                print(error)
        # Pushing content.
        else:
            try:
                cloneURL = self.githubAPI.getRepoCloneURL(repoName)
                exitCode = CommandRunner.gitLocalToRemote(cloneURL)
                if exitCode == 0:
                    print(
                        f"\n{GREEN}[SUCCESS]{RESET} Pushed content to repository with success!")
                    createRepoFile(repoPath=getcwd(), repoName=repoName)
                else:
                    print(
                        f"\n{RED}[ERROR]{RESET} Unnable to push content to repository.")
            except Exception as error:
                print(error)
        # Collaborators.
        for i in range(yaml.collaboratorsCount()):
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
        chooser = FileChooser(TEMPLATES_PATH)
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
        chooser = FileChooser(TEMPLATES_PATH)
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
        chooser = FileChooser(TEMPLATES_PATH)
        if not templateName.endswith(".yaml"):
            templateName += ".yaml"
        filePath = chooser.getFilePathByName(templateName)
        exitCode = CommandRunner.openFileInTextEditor(filePath)
        if exitCode == 0:
            return True
        print(
            f"\n{RED}[ERROR]{RESET} Unnable to edit template, make sure the file exists.")
        return False

    # Delete.
    def delete(self, templateName: str) -> bool:
        if templateName == "all":
            FileDeleter.deleteAllFromFolder(TEMPLATES_PATH)
            print(
                f"\n{GREEN}[SUCCESS]{RESET} Templates cleared!")
            return True
        else:
            if not templateName.endswith(".yaml"):
                templateName += ".yaml"
            filePath = f"{TEMPLATES_PATH}/{templateName}"
            deleted = FileDeleter.deleteFile(filePath)
            if deleted:
                print(
                    f"\n{GREEN}[SUCCESS]{RESET} Template deleted with success!")
                return True
            print(
                f"\n{RED}[ERROR]{RESET} Unnable to delete template, make sure the file exists.")
            return False

    # Generate.
    def generate(self) -> bool:
        print(
            f"\n{CYAN}This is the name of the template YAML file (my-template -> my-template.yaml).{RESET}")
        templateNameInput = input("Template name: ")
        templateName = sub(TEMPLATE_NAME_PATTERN, '-', templateNameInput)
        if templateNameInput != templateName:
            print(
                f"\n{YELLOW}[WARN]{RESET} Template name was changed to -> {templateName}")
        if not templateName.endswith(".yaml"):
            templateName += ".yaml"
        repoNameInput = input("\nRepository name: ")
        repoName = sub(REPOSITORY_NAME_PATTERN, '-', repoNameInput)
        if repoNameInput != repoName:
            print(
                f"\n{YELLOW}[WARN]{RESET} Repository name was changed to -> {repoName}\n")
        while len(repoName) == 0:
            print("Invalid repository name.")
            repoName = input("Repository name: ")
        repoDescription = input("Repository description: ")
        private = input(
            "Should the repository be private? (Y/y = Yes, Others = No): ")
        private = True if private.upper() == "Y" else False
        print(
            f"\n{CYAN}This will send the contents of your current directory to the repository.{RESET}")
        includeContent = input("Include content? (Y/y = Yes, Others = No): ")
        includeContent = True if includeContent.upper() == "Y" else False
        addCollaborators = input(
            "\nAdd collaborators? (Y/y = Yes, Others = No): ")
        collaborators = []
        if addCollaborators.upper() == "Y":
            while True:
                collaboratorName = input("\n  Collaborator name: ")
                permissionOptions = ["admin", "push", "pull"]
                collaboratorPermission = input(
                    "  Collaborator permission (admin [default], push or pull): ") or "admin"
                while not collaboratorPermission.lower() in permissionOptions:
                    print("  Invalid permission.")
                    collaboratorPermission = input(
                        "  Collaborator permission (admin [default], push or pull): ") or "admin"
                collaborators.append(
                    {"name": collaboratorName, "permission": collaboratorPermission})
                continueAdding = input(
                    "\nContinue adding collaborators? (Y/y/Enter = Yes, Others = No): ")
                if not continueAdding.upper() == "Y" and not len(continueAdding) == 0:
                    break
        writer = YAMLWriter(TEMPLATES_PATH)
        wrote = writer.writeTemplate(
            templateName=templateName,
            repoName=repoName,
            repoDescription=repoDescription,
            private=private,
            includeContent=includeContent,
            collaborators=collaborators
        )
        if wrote:
            print(
                f"\n{GREEN}[SUCCESS]{RESET} Template {templateName} generated with success!")
            return True
        print(
            f"\n{RED}[ERROR]{RESET} Unnable to generate template.")
        return False

    # Merge.
    def merge(self, templateNames: "tuple[str]") -> bool:
        if len(templateNames) < 2:
            print(
                f"\n{RED}[ERROR]{RESET} At least 2 template names must be specified.")
            return False
        chooser = FileChooser(TEMPLATES_PATH)
        inputedTemplateName = input("\nEnter the new template name: ")
        if not inputedTemplateName.endswith(".yaml"):
            inputedTemplateName += ".yaml"
        repoName = "Merged-Repository"
        repoDescription = "This is a description!"
        private = None
        privateConflicted = False
        includeContent = None
        includeContentConflicted = False
        mergedCollaborators = []
        namesAdded = []
        for templateName in templateNames:
            if not templateName.endswith(".yaml"):
                templateName += ".yaml"
            filePath = chooser.getFilePathByName(templateName)
            if filePath is None:
                print(
                    f"\n{RED}[ERROR]{RESET} Template {templateName} not found.")
                return False
            parser = YAMLParser(filePath)
            yaml = YAMLInterpreter(parser)
            if private is not None and yaml.private() != private and not privateConflicted:
                privateConflicted = True
                newPrivate = input(
                    f"\nRepository visibility {YELLOW}conflicted{RESET}, use T/t for private or F/f for public: ")
                private = True if newPrivate.upper() == "T" else False
            elif private is None:
                private = yaml.private()
            if includeContent is not None and yaml.includeContent(
            ) != includeContent and not includeContentConflicted:
                includeContentConflicted = True
                newIncludeContent = input(
                    f"\nInclude content {YELLOW}conflicted{RESET}, use T/t to include or F/f to not include: ")
                includeContent = True if newIncludeContent.upper() == "T" else False
            elif includeContent is None:
                includeContent = yaml.includeContent()
            for i in range(yaml.collaboratorsCount()):
                collaboratorName = yaml.collaboratorName(i)
                collaboratorPermission = yaml.collaboratorPermission(i)
                if collaboratorName not in namesAdded:
                    data = {
                        "name": collaboratorName,
                        "permission": collaboratorPermission
                    }
                    mergedCollaborators.append(data)
                    namesAdded.append(collaboratorName)
        writer = YAMLWriter(TEMPLATES_PATH)
        wrote = writer.writeTemplate(
            templateName=inputedTemplateName,
            repoName=repoName,
            repoDescription=repoDescription,
            private=private,
            includeContent=includeContent,
            collaborators=mergedCollaborators
        )
        if wrote:
            print(
                f"\n{GREEN}[SUCCESS]{RESET} Templates merged with success!")
            return True
        print(
            f"\n{RED}[ERROR]{RESET} Unnable to merge templates.")
        return False

    # Version.
    def version(self, repoPath: str) -> bool:
        version = CommandRunner.getGRCCurrentVersion(repoPath)
        if version is None:
            print(
                f"\n{RED}[ERROR]{RESET} Unnable to get GRC current version.")
            return False
        print(f"\nGRC version {version}\n")
        return True

    # Update.
    def update(self, repoPath: str) -> bool:
        currentVersion = CommandRunner.getGRCCurrentVersion(repoPath)
        if currentVersion is None:
            print(
                f"\n{RED}[ERROR]{RESET} Unnable to get GRC current version.")
            return False
        latestVersionInfo = checkIfLatestVersion(currentVersion)
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
            return False
        print("\nAlready using GRC latest version.")
        return False

    # List Repos.
    def listRepos(self) -> None:
        chooser = FileChooser(REPOSITORIES_PATH)
        fileNames = chooser.getFileNames()
        if len(fileNames) <= 0:
            print("No repositories to list.\n")
            return
        for fileName in fileNames:
            print(fileName.replace(".yaml", ""))
        print("")

    # Get Repo.
    def getRepo(self, repoName: str) -> bool:
        chooser = FileChooser(REPOSITORIES_PATH)
        if not repoName.endswith(".yaml"):
            repoName += ".yaml"
        content = chooser.getFileContentByName(repoName)
        if content is None:
            print(
                f"\n{RED}[ERROR]{RESET} Repository not found.")
            return False
        print(f"\n{content}")
        return True

    # Open Repo.
    def openRepo(self, repoName: str) -> bool:
        chooser = FileChooser(REPOSITORIES_PATH)
        if not repoName.endswith(".yaml"):
            repoName += ".yaml"
        filePath = chooser.getFilePathByName(repoName)
        if filePath is None:
            print(
                f"\n{RED}[ERROR]{RESET} Repository '{repoName}' not found.")
            return False
        parser = YAMLParser(filePath)
        interpreter = YAMLInterpreter(parser)
        repoPath = interpreter.repoPath()
        exitCode = CommandRunner.code(repoPath)
        if exitCode != 0:
            print(
                f"\n{RED}[ERROR]{RESET} You don't have VSCode installed in your machine.")
            return False
        return True

    # Remove Repo.
    def removeRepo(self, fileName: str) -> bool:
        if fileName == "all":
            FileDeleter.deleteAllFromFolder(REPOSITORIES_PATH)
            print(
                f"\n{GREEN}[SUCCESS]{RESET} Repositories cleared!")
            return True
        else:
            if not fileName.endswith(".yaml"):
                fileName += ".yaml"
            filePath = f"{REPOSITORIES_PATH}/{fileName}"
            deleted = FileDeleter.deleteFile(filePath)
            if deleted:
                print(
                    f"\n{GREEN}[SUCCESS]{RESET} Repository removed with success!")
                return True
            print(
                f"\n{RED}[ERROR]{RESET} Unnable to remove repository, make sure it exists.")
            return False

    # Add Collab.
    def addCollab(self, collaboratorName: str, repoName: str, permission: str):
        if self.githubAPI is None or not self.githubAPI.isAuthenticated():
            print(
                f"\nUser not authenticated to GitHub, run '{CYAN}grc{RESET} authenticate <YOUR_ACCESS_TOKEN>' to authenticate.")
            return False
        try:
            self.githubAPI.addCollaborator(
                repoName=repoName,
                collaboratorName=collaboratorName,
                permission=permission)
            return True
        except BaseException:
            print(
                f"\n{RED}[ERROR]{RESET} Unnable to add collaborator to repository {repoName}.")
            return False

    # Remote Repos.
    def remoteRepos(self) -> None:
        if self.githubAPI is None or not self.githubAPI.isAuthenticated():
            print(
                f"\nUser not authenticated to GitHub, run '{CYAN}grc{RESET} authenticate <YOUR_ACCESS_TOKEN>' to authenticate.")
            return False
        try:
            repoList = self.githubAPI.getRepoList()
            if len(repoList) == 0:
                print("\nNo repositories to list.")
                return
            print("")
            for repo in repoList:
                print(repo)
        except Exception as error:
            print(error)

    # Clone.
    def clone(self, repoName: str) -> bool:
        if self.githubAPI is None or not self.githubAPI.isAuthenticated():
            print(
                f"\nUser not authenticated to GitHub, run '{CYAN}grc{RESET} authenticate <YOUR_ACCESS_TOKEN>' to authenticate.")
            return False
        try:
            cloneURL = self.githubAPI.getRepoCloneURL(repoName)
            exitCode = CommandRunner.gitClone(cloneURL)
            if exitCode == 0:
                print(
                    f"\n{GREEN}[SUCCESS]{RESET} Repository cloned with success!")
                createRepoFile(repoPath=f"{getcwd()}/{repoName}")
                return True
            print(
                f"\n{RED}[ERROR]{RESET} Unnable to clone repository.")
            return False
        except BaseException:
            print(
                f"\n{RED}[ERROR]{RESET} Unnable to clone repository {repoName}.")
            return False

    # Help
    def help(self) -> None:
        print(
            "\nWhat is GRC?\nGRC is a tool to automatically create GitHub repositories using YAML templates.")
        print(
            f"\n{HEADER}--{RESET} General Commands {HEADER}--{RESET}")
        print(
            f"\n{BLUE}help{RESET}\nShows this message.")
        print(
            f"\n{BLUE}authenticate{RESET} {CYAN}<ACCESS_TOKEN>{RESET}\nAuthenticates to GitHub in order to create repositories in your account.")
        print(
            f"\n{BLUE}version{RESET}\nShows you the GRC version that you are currently using.")
        print(
            f"\n{BLUE}update{RESET}\nAutomatically installs the latest GRC version in case you're still not using it.")
        print(
            f"\n{HEADER}--{RESET} Templates Commands {HEADER}--{RESET}")
        print(
            f"\n{HEADER}[VERY USEFUL] {RESET}{BLUE}temp generate{RESET}\nGenerates a template for you with the data that you input.")
        print(
            f"\n{HEADER}[VERY USEFUL] {RESET}{BLUE}temp choose{RESET}\nLets you choose a file from your saved templates to create a repository based on it.")
        print(
            f"\n{BLUE}temp list{RESET}\nLists all the templates that are saved in your machine.")
        print(
            f"\n{BLUE}temp get{RESET} {CYAN}<TEMPLATE_NAME>{RESET}\nShows the content of a template that is saved in your machine.")
        print(
            f"\n{BLUE}temp edit{RESET} {CYAN}<TEMPLATE_NAME>{RESET}\nOpens a text editor and lets you edit one of your saved templates.")
        print(
            f"\n{BLUE}temp delete{RESET} {CYAN}<TEMPLATE_NAME>{RESET}\nDeletes a template from your saved templates.\n(Use 'delete all' to delete all your templates).")
        print(
            f"\n{BLUE}temp merge{RESET} {CYAN}<TEMPLATE_NAME_1>{RESET} {CYAN}<TEMPLATE_NAME_2> ...{RESET}\nMerges *N* templates and creates a new template with all the collaborators included.")
        print(
            f"\n{BLUE}temp apply{RESET} {CYAN}<PATH_TO_YOUR_YAML_FILE>{RESET}\nCreates a repository for you based on a YAML file that is passed as a parameter.")
        print(
            f"\n{BLUE}temp save{RESET} {CYAN}<PATH_TO_YOUR_YAML_FILE>{RESET}\nSaves a YAML file to your templates, so that you can later use it to create another repository with the same configurations.")
        print(
            f"\n{HEADER}--{RESET} Repositories Commands {HEADER}--{RESET}")
        print(
            f"\n{BLUE}repo list{RESET}\nLists all the repositories that you have created with GRC.")
        print(
            f"\n{BLUE}repo get{RESET} {CYAN}<REPO_NAME>{RESET}\nShows information about a specific repository that was created with GRC.")
        print(
            f"\n{BLUE}repo open{RESET} {CYAN}<REPO_NAME>{RESET}\nOpens the specified repository in Visual Studio Code.")
        print(
            f"\n{BLUE}repo remove{RESET} {CYAN}<REPO_NAME>{RESET}\nRemoves a repository from your repositories list.\n(Use 'remove-repo all' to remove all your repositories).")
        print(
            f"\n{HEADER}--{RESET} Remote Repositories Commands {HEADER}--{RESET}")
        print(
            f"\n{BLUE}remote add-collab{RESET} {CYAN}<REPO_NAME>{RESET} {CYAN}<USER_NAME>{RESET} {CYAN}<PERMISSION?>{RESET}\nAdds a collaborator to a repository.")
        print(
            f"\n{BLUE}remote list{RESET}\nLists all the remote repositories that you have in your GitHub account.")
        print(
            f"\n{BLUE}remote clone{RESET} {CYAN}<REPO_NAME>{RESET}\nClones a personal repository from your GitHub account.\n")
