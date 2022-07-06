import click
from os import path
from modules.token import TokenManager
from modules.version import VersionManager
from modules.cli import CLI, checkIfLatestVersion
from modules.terminal_commands import CommandRunner
from modules.coloring import Colors

cliInstance = None
tokenManager = None

YELLOW = Colors.YELLOW
CYAN = Colors.CYAN
RESET = Colors.RESET


# [Main command group].


@click.group()
def cli() -> None:
    pass


# Help.
@click.command(name="help")
def help() -> None:
    success = cliInstance.help()
    exit(0 if success else 1)


# Authenticate.
@click.command(name="authenticate")
@click.argument("access_token")
def authenticate(access_token: str) -> None:
    success = cliInstance.authenticate(access_token, logs=True)
    print("")
    exit(0 if success else 1)


# User.
@click.command(name="user")
def user() -> None:
    success = cliInstance.user()
    print("")
    exit(0 if success else 1)


# Version.
@click.command(name="version")
def version() -> None:
    repoPath = path.abspath(path.join(path.dirname(__file__), "../"))
    success = cliInstance.version(repoPath)
    exit(0 if success else 1)


# Update.
@click.command(name="update")
def update() -> None:
    repoPath = path.abspath(path.join(path.dirname(__file__), "../"))
    success = cliInstance.update(repoPath)
    print("")
    exit(0 if success else 1)


# [Templates command group].


@click.group()
def temp() -> None:
    pass


# Temp Save.
@temp.command(name="save")
@click.argument("file_path")
def save(file_path: str) -> None:
    success = cliInstance.save(file_path)
    print("")
    exit(0 if success else 1)


# Temp Choose.
@temp.command(name="choose")
@click.argument("template_name", required=False)
@click.option("-n", "--name")
@click.option("-d", "--description")
@click.option("-p", "--private")
@click.option("-i", "--include_content")
def choose(
        template_name: str = None,
        name: str = None,
        description: str = None,
        private: str = None,
        include_content: str = None) -> None:
    if private is not None:
        if private == "true":
            private = True
        else:
            private = False
    if include_content is not None:
        if include_content == "true":
            include_content = True
        else:
            include_content = False
    success = cliInstance.choose(
        template_name, name, description, private, include_content)
    print("")
    exit(0 if success else 1)


# Temp Apply.
@temp.command(name="apply")
@click.argument("file_path")
def apply(file_path: str) -> None:
    success = cliInstance.apply(file_path)
    print("")
    exit(0 if success else 1)


# Temp List.
@temp.command(name="list")
def list() -> None:
    success = cliInstance.list()
    print("")
    exit(0 if success else 1)


# Temp Get.
@temp.command(name="get")
@click.argument("template_name")
def get(template_name: str) -> None:
    success = cliInstance.get(template_name)
    print("")
    exit(0 if success else 1)


# Temp Edit.
@temp.command(name="edit")
@click.argument("template_name")
def edit(template_name: str) -> None:
    success = cliInstance.edit(template_name)
    print("")
    exit(0 if success else 1)


# Temp Delete.
@temp.command(name="delete")
@click.argument("template_name")
def delete(template_name: str) -> None:
    success = cliInstance.delete(template_name)
    print("")
    exit(0 if success else 1)


# Temp Generate.
@temp.command(name="generate")
def generate() -> None:
    success = cliInstance.generate()
    print("")
    exit(0 if success else 1)


# Temp Merge.
@temp.command(name="merge")
@click.argument("template_names", nargs=-1)
def merge(template_names: "tuple[str]") -> None:
    success = cliInstance.merge(template_names)
    print("")
    exit(0 if success else 1)


# [GRC Repositories command group].


@click.group()
def repo() -> None:
    pass


# Repo List.
@repo.command(name="list")
def listRepos() -> None:
    print("")
    success = cliInstance.listRepos()
    exit(0 if success else 1)


# Repo Get.
@repo.command(name="get")
@click.argument("repo_name")
def getRepo(repo_name: str) -> None:
    success = cliInstance.getRepo(repo_name)
    print("")
    exit(0 if success else 1)


# Repo Open.
@repo.command(name="open")
@click.argument("repo_name")
def openRepo(repo_name: str) -> None:
    success = cliInstance.openRepo(repo_name)
    print("")
    exit(0 if success else 1)


# Repo Remove.
@repo.command(name="remove")
@click.argument("repo_name")
def removeRepo(repo_name: str) -> None:
    success = cliInstance.removeRepo(repo_name)
    print("")
    exit(0 if success else 1)


# [Remote repositories command group].


@click.group()
def remote() -> None:
    pass


# Remote Add-Collab.
@remote.command(name="add-collab")
@click.argument("collaborator_name")
@click.argument("repo_name")
@click.argument("permission", default="admin")
def addCollab(collaborator_name: str, repo_name: str, permission: str) -> None:
    success = cliInstance.addCollab(collaborator_name, repo_name, permission)
    print("")
    exit(0 if success else 1)


# Remote List.
@remote.command(name="list")
def remoteRepos() -> None:
    success = cliInstance.remoteRepos()
    print("")
    exit(0 if success else 1)


# Remote Clone.
@remote.command(name="clone")
@click.argument("repo_name")
def clone(repo_name: str) -> None:
    success = cliInstance.clone(repo_name)
    print("")
    exit(0 if success else 1)


# Remote URL.
@remote.command(name="url")
@click.argument("repo_name")
def url(repo_name: str) -> None:
    success = cliInstance.url(repo_name)
    print("")
    exit(0 if success else 1)


# Function to setup all the commands.
def setupCommands() -> None:
    # General.
    cli.add_command(help)
    cli.add_command(authenticate)
    cli.add_command(user)
    cli.add_command(version)
    cli.add_command(update)
    # Templates.
    cli.add_command(temp)
    # GRC Repositories.
    cli.add_command(repo)
    # Remote repositories.
    cli.add_command(remote)


# Function that warns the user if they are not using the latest GRC version.
def versionLog(versionManager: VersionManager) -> None:
    repoPath = path.abspath(path.join(path.dirname(__file__), "../"))
    currentVersion = CommandRunner.getGRCCurrentVersion(repoPath)
    versionManager.writeVersion(currentVersion)
    versionInfo = checkIfLatestVersion(currentVersion)
    isLatestVersion = versionInfo[0]
    latestVersion = versionInfo[1]
    if not isLatestVersion:
        print(
            f"\n{YELLOW}[WARN]{RESET} A newer version of GRC is disponible [{latestVersion}], run '{CYAN}grc{RESET} update' to get it.")


if __name__ == "__main__":
    cliInstance = CLI()
    tokenManager = TokenManager()
    accessToken = tokenManager.readToken()
    cliInstance.authenticate(accessToken, logs=False)
    versionManager = VersionManager(daysInCache=0.1)
    if versionManager.shouldResetCache():
        versionLog(versionManager)
    setupCommands()
    cli()
