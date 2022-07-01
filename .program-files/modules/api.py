from github import Github
from .coloring import Colors

GREEN = Colors.GREEN
RED = Colors.RED
RESET = Colors.RESET


class GitHubAPI:
    def __init__(self, accessToken: str) -> None:
        try:
            self.github = Github(accessToken, verify=True)
            # Will raise an error if the access token is invalid.
            self.github.get_user().get_repos().totalCount
        except BaseException:
            raise Exception(f"\n{RED}[ERROR]{RESET} Invalid access token.")

    def isAuthenticated(self) -> bool:
        try:
            # Will raise an error if the user is not authenticated.
            self.github.get_user().get_repos().totalCount
            return True
        except BaseException:
            return False

    def getRepoList(self) -> list:
        user = self.github.get_user()
        try:
            return [repo.name for repo in user.get_repos()]
        except BaseException:
            raise Exception(
                f"\n{RED}[ERROR]{RESET} Unable to get list of repositories.")

    def createRepo(
            self,
            name: str,
            description: str,
            private: bool,
            createREADME: bool = False) -> bool:
        user = self.github.get_user()
        try:
            user.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=createREADME,
            )
        except BaseException:
            raise Exception(
                f"\n{RED}[ERROR]{RESET} Unnable to create repository '{name}'.")

    def addCollaborator(
            self,
            repoName: str,
            collaboratorName: str,
            permission: str) -> bool:
        user = self.github.get_user()
        try:
            repo = user.get_repo(repoName)
            repo.add_to_collaborators(
                collaborator=collaboratorName,
                permission=permission
            )
            print(
                f"\n{GREEN}[SUCCESS]{RESET} Added collaborator '{collaboratorName}' to repository '{repoName}'.")
        except BaseException:
            raise Exception(
                f"\n{RED}[ERROR]{RESET} Unnable to add collaborator '{collaboratorName}' to repository.")

    def getRepoCloneURL(self, repoName: str) -> str:
        user = self.github.get_user()
        try:
            repo = user.get_repo(repoName)
            return repo.clone_url
        except BaseException:
            raise Exception(
                f"\n{RED}[ERROR]{RESET} Unnable to get '{repoName}' repository clone URL.")

    @staticmethod
    def getGRCLatestTag() -> str:
        try:
            github = Github()
            repo = github.get_repo(
                "ArthurSudbrackIbarra/GitHub-Repo-Creator")
            tags = repo.get_tags()
            tagNames = []
            for tag in tags:
                if tag.name.startswith("v"):
                    tagNames.append(tag.name)
                if len(tagNames) > 0:
                    return tagNames[0]
            return None
        except BaseException:
            raise Exception(
                f"\n{RED}[ERROR]{RESET} Unnable to get GRC repository latest tag.")
