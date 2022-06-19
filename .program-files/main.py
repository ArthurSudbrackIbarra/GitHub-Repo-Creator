from os import path
import click
from modules.tokens import TokenManager
from modules.version import VersionManager
from modules.clis import CLI
from modules.terminal_commands import CommandRunner
from modules.coloring import Colors

cli = None
tokenManager = None

YELLOW = Colors.YELLOW
CYAN = Colors.CYAN
RESET = Colors.RESET


# Main.
@click.group()
def main() -> None:
    pass


# Authenticate.
@click.command(name="authenticate")
@click.argument("access_token")
def authenticate(access_token: str) -> None:
    cli.authenticate(access_token, logs=True)
    print("")


# Save.
@click.command(name="save")
@click.argument("absolute_file_path")
def save(absolute_file_path: str) -> None:
    cli.save(absolute_file_path)
    print("")


# Choose.
@click.command(name="choose")
@click.argument("template_name", required=False)
@click.option("-p", "--private")
@click.option("-i", "--include_content")
def choose(template_name: str = None, private: str = None, include_content: str = None) -> None:
    if private is not None:
        if private == "true":
            private = True
        elif private == "false":
            private = False
    if include_content is not None:
        if include_content == "true":
            include_content = True
        elif include_content == "false":
            include_content = False
    cli.choose(template_name, private, include_content)
    print("")


# Create.
@click.command(name="create")
@click.argument("absolute_file_path")
def create(absolute_file_path: str) -> None:
    cli.create(absolute_file_path)
    print("")


# List.
@click.command(name="list")
def list() -> None:
    cli.list()
    print("")


# Get.
@click.command(name="get")
@click.argument("template_name")
def get(template_name: str) -> None:
    cli.get(template_name)
    print("")


# Edit.
@click.command(name="edit")
@click.argument("template_name")
def edit(template_name: str) -> None:
    cli.edit(template_name)
    print("")


# Delete.
@click.command(name="delete")
@click.argument("template_name")
def delete(template_name: str) -> None:
    cli.delete(template_name)
    print("")


# Generate.
@click.command(name="generate")
def generate() -> None:
    cli.generate()
    print("")


# Merge.
@click.command(name="merge")
@click.argument("template_names", nargs=-1)
def merge(template_names: "tuple[str]") -> None:
    cli.merge(template_names)
    print("")


# Version.
@click.command(name="version")
def version() -> None:
    repoPath = path.abspath(path.join(path.dirname(__file__), "../"))
    cli.version(repoPath)


# Update.
@click.command(name="update")
def update() -> None:
    repoPath = path.abspath(path.join(path.dirname(__file__), "../"))
    cli.update(repoPath)
    print("")


# List-Repos.
@click.command(name="list-repos")
def listRepos() -> None:
    print("")
    cli.listRepos()


# Get-Repo.
@click.command(name="get-repo")
@click.argument("repo_name")
def getRepo(repo_name: str) -> None:
    cli.getRepo(repo_name)
    print("")


# Open-Repo.
@click.command(name="open-repo")
@click.argument("repo_name")
def openRepo(repo_name: str) -> None:
    cli.openRepo(repo_name)
    print("")


# Remove-Repo.
@click.command(name="remove-repo")
@click.argument("repo_name")
def removeRepo(repo_name: str) -> None:
    cli.removeRepo(repo_name)
    print("")


# Help.
@click.command(name="help")
def help() -> None:
    cli.help()


# Function to add all the commands.
def addCommands() -> None:
    main.add_command(authenticate)
    main.add_command(save)
    main.add_command(choose)
    main.add_command(create)
    main.add_command(list)
    main.add_command(get)
    main.add_command(edit)
    main.add_command(delete)
    main.add_command(generate)
    main.add_command(merge)
    main.add_command(version)
    main.add_command(update)
    main.add_command(listRepos)
    main.add_command(getRepo)
    main.add_command(openRepo)
    main.add_command(removeRepo)
    main.add_command(help)


# Function that warns the user if they are not using the latest GRC version.
def versionLog(versionManager: VersionManager) -> None:
    print("\nChecking GRC version...")
    repoPath = path.abspath(path.join(path.dirname(__file__), "../"))
    currentVersion = CommandRunner.getGRCCurrentVersion(repoPath)
    versionManager.writeVersion(currentVersion)
    versionInfo = cli.isLatestVersion(currentVersion)
    isLatestVersion = versionInfo[0]
    latestVersion = versionInfo[1]
    if not isLatestVersion:
        print(
            f"\n{YELLOW}[WARN]{RESET} A newer version of GRC is disponible [{latestVersion}], run '{CYAN}grc{RESET} update' to get it.")


if __name__ == "__main__":
    cli = CLI()
    tokenManager = TokenManager()
    token = tokenManager.readToken()
    cli.authenticate(token, logs=False)
    # 0.08 days = 1,92 hours.
    versionManager = VersionManager(daysInCache=0.08)
    if versionManager.shouldResetCache():
        versionLog(versionManager)
    addCommands()
    main()
