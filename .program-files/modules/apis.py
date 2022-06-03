from github import Github


class GitHubAPI:
    def __init__(self, accessToken: str) -> None:
        try:
            self.github = Github(accessToken)
        except Exception as error:
            print(error)
            raise Exception("Invalid access token.")

    def createRepo(self, name: str, description: str, private: bool) -> bool:
        user = self.github.get_user()
        try:
            user.create_repo(
                name=name,
                description=description,
                private=private
            )
        except Exception as error:
            print(error)
            raise Exception("Unnable to create repository!")

    def addCollaborator(self, repoName: str, collaboratorName: str, permission: str) -> bool:
        user = self.github.get_user()
        try:
            repo = user.get_repo(repoName)
            repo.add_to_collaborators(
                collaborator=collaboratorName,
                permission=permission
            )
        except Exception as error:
            print(error)
            raise Exception("Unnable to add collaborator(s) to repository.")
