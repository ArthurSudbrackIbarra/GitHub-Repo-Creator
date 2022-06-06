import click
from modules.tokens import TokenManager
from modules.clis import CLI

cli = None
tokenManager = None


# Main.
@click.group(help="Automatically create GitHub repositories.")
def main() -> None:
    pass


# Authenticate.
@click.command(name="authenticate")
@click.argument("access_token")
def authenticate(access_token: str) -> None:
    global cli
    cli.authenticate(access_token, logs=True)
    print("")


# Save.
@click.command(name="save")
@click.argument("absolute_file_path")
def save(absolute_file_path: str) -> None:
    global cli
    cli.save(absolute_file_path)
    print("")


# Choose.
@click.command(name="choose")
def choose() -> None:
    global cli
    cli.choose()
    print("")


# Create.
@click.command(name="create")
@click.argument("absolute_file_path")
def create(absolute_file_path: str) -> None:
    global cli
    cli.create(absolute_file_path)
    print("")


# List.
@click.command(name="list")
def list() -> None:
    global cli
    cli.list()
    print("")


# Get.
@click.command(name="get")
@click.argument("template_name")
def get(template_name: str) -> None:
    global cli
    cli.get(template_name)


# Edit.
@click.command(name="edit")
@click.argument("template_name")
def edit(template_name: str) -> None:
    global cli
    cli.edit(template_name)
    print("")


# Delete.
@click.command(name="delete")
@click.argument("template_name")
def delete(template_name: str) -> None:
    global cli
    cli.delete(template_name)
    print("")


# Update.
@click.command(name="update")
def update() -> None:
    global cli
    cli.update()
    print("")


if __name__ == "__main__":
    main.add_command(authenticate)
    main.add_command(save)
    main.add_command(choose)
    main.add_command(create)
    main.add_command(list)
    main.add_command(get)
    main.add_command(edit)
    main.add_command(delete)
    main.add_command(update)
    cli = CLI()
    tokenManager = TokenManager()
    token = tokenManager.readToken()
    cli.authenticate(token, logs=False)
    main()
