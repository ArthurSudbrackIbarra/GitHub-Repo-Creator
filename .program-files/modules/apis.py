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
        except:
            raise Exception(f"\n{RED}[ERROR]{RESET} Invalid access token.")

    def createRepo(self, name: str, description: str, private: bool) -> bool:
        user = self.github.get_user()
        try:
            user.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=True
            )
        except:
            raise Exception(
                f"\n{RED}[ERROR]{RESET} Unnable to create repository '{name}'.")

    def addCollaborator(self, repoName: str, collaboratorName: str, permission: str) -> bool:
        user = self.github.get_user()
        try:
            repo = user.get_repo(repoName)
            repo.add_to_collaborators(
                collaborator=collaboratorName,
                permission=permission
            )
            print(
                f"\n{GREEN}[SUCCESS]{RESET} Added collaborator '{collaboratorName}' to repository.")
        except:
            raise Exception(
                f"\n{RED}[ERROR]{RESET} Unnable to add collaborator '{collaboratorName}' to repository.")

    def getRepoCloneURL(self, repoName: str) -> str:
        user = self.github.get_user()
        try:
            repo = user.get_repo(repoName)
            return repo.clone_url
        except:
            raise Exception(
                f"\n{RED}[ERROR]{RESET} Unnable to get '{repoName}' repository clone URL.")
