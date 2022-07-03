from os import path
import click
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
    cliInstance.help()


# Authenticate.
@click.command(name="authenticate")
@click.argument("access_token")
def authenticate(access_token: str) -> None:
    cliInstance.authenticate(access_token, logs=True)
    print("")


# Version.
@click.command(name="version")
def version() -> None:
    repoPath = path.abspath(path.join(path.dirname(__file__), "../"))
    cliInstance.version(repoPath)


# Update.
@click.command(name="update")
def update() -> None:
    repoPath = path.abspath(path.join(path.dirname(__file__), "../"))
    cliInstance.update(repoPath)
    print("")


# [Templates command group].


@click.group()
def temp() -> None:
    pass


# Temp Save.
@temp.command(name="save")
@click.argument("file_path")
def save(file_path: str) -> None:
    cliInstance.save(file_path)
    print("")


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
    cliInstance.choose(template_name, name, description,
                       private, include_content)
    print("")


# Temp Apply.
@temp.command(name="apply")
@click.argument("file_path")
def apply(file_path: str) -> None:
    cliInstance.apply(file_path)
    print("")


# Temp List.
@temp.command(name="list")
def list() -> None:
    cliInstance.list()
    print("")


# Temp Get.
@temp.command(name="get")
@click.argument("template_name")
def get(template_name: str) -> None:
    cliInstance.get(template_name)
    print("")


# Temp Edit.
@temp.command(name="edit")
@click.argument("template_name")
def edit(template_name: str) -> None:
    cliInstance.edit(template_name)
    print("")


# Temp Delete.
@temp.command(name="delete")
@click.argument("template_name")
def delete(template_name: str) -> None:
    cliInstance.delete(template_name)
    print("")


# Temp Generate.
@temp.command(name="generate")
def generate() -> None:
    cliInstance.generate()
    print("")


# Temp Merge.
@temp.command(name="merge")
@click.argument("template_names", nargs=-1)
def merge(template_names: "tuple[str]") -> None:
    cliInstance.merge(template_names)
    print("")


# [GRC Repositories command group].


@click.group()
def repo() -> None:
    pass


# Repo List.
@repo.command(name="list")
def listRepos() -> None:
    print("")
    cliInstance.listRepos()


# Repo Get.
@repo.command(name="get")
@click.argument("repo_name")
def getRepo(repo_name: str) -> None:
    cliInstance.getRepo(repo_name)
    print("")


# Repo Open.
@repo.command(name="open")
@click.argument("repo_name")
def openRepo(repo_name: str) -> None:
    cliInstance.openRepo(repo_name)
    print("")


# Repo Remove.
@repo.command(name="remove")
@click.argument("repo_name")
def removeRepo(repo_name: str) -> None:
    cliInstance.removeRepo(repo_name)
    print("")


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
    cliInstance.addCollab(collaborator_name, repo_name, permission)
    print("")


# Remote List.
@remote.command(name="list")
def remoteRepos() -> None:
    cliInstance.remoteRepos()
    print("")


# Remote Clone.
@remote.command(name="clone")
@click.argument("repo_name")
def clone(repo_name: str) -> None:
    cliInstance.clone(repo_name)
    print("")


# Remote URL.
@remote.command(name="url")
@click.argument("repo_name")
def url(repo_name: str) -> None:
    cliInstance.url(repo_name)
    print("")


# Function to add all the commands.
def addCommands() -> None:
    # General.
    cli.add_command(help)
    cli.add_command(authenticate)
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
    token = tokenManager.readToken()
    cliInstance.authenticate(token, logs=False)
    versionManager = VersionManager(daysInCache=0.08)
    if versionManager.shouldResetCache():
        versionLog(versionManager)
    addCommands()
    cli()
