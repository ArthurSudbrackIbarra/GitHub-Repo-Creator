from os import path
import click
from modules.tokens import TokenManager
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
def choose() -> None:
    cli.choose()
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


# Version.
@click.command(name="version")
@click.argument("repo_path")
def update(repo_path: str) -> None:
    cli.version(repo_path)
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
    main.add_command(version)
    main.add_command(update)
    main.add_command(help)


# Function warns the user if they are not using the latest GRC version.
def versionLog() -> None:
    repoPath = path.abspath(path.join(path.dirname(__file__), "../"))
    currentVersion = CommandRunner.getGRCCurrentVersion(repoPath)
    isLatestVersion = cli.isLatestVersion(currentVersion)[0]
    if not isLatestVersion:
        print(
            f"\n{YELLOW}[WARN]{RESET} A newer version of GRC is disponible, run '{CYAN}grc{RESET} update' to get it.")


if __name__ == "__main__":
    cli = CLI()
    tokenManager = TokenManager()
    token = tokenManager.readToken()
    cli.authenticate(token, logs=False)
    versionLog()
    addCommands()
    main()
