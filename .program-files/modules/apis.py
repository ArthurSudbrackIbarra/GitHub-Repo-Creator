from github import Github


class GitHubAPI:
    def __init__(self, accessToken: str) -> None:
        self.github = Github(accessToken)

    def createRepo(self, name: str, description: str, private: bool) -> bool:
        user = self.github.get_user()
        user.create_repo(
            name=name,
            description=description,
            private=private
        )

    def addCollaborator(self, name: str, permission: str) -> bool:
        repo = self.github.get_repo(name)
        repo.add_to_collaborators(
            collaborator=name,
            permission=permission
        )
