import click
from modules.tokens import TokenManager
from modules.clis import CLI

cli = None
tokenManager = None


# Main.
@click.group(help="Automatically create GitHub repositories.")
def main() -> None:
    pass


# Set token.
@click.command(name="authenticate")
@click.argument("access_token")
def authenticate(access_token: str) -> None:
    global cli
    cli.authenticate(access_token, logs=True)


# Template.
@click.command(name="template")
@click.argument("template_type")
def template(template_type: str) -> None:
    global cli
    cli.template(template_type)


# Create.
@click.command(name="create")
@click.argument("absolute_file_path")
def create(absolute_file_path: str) -> None:
    global cli
    created = cli.create(absolute_file_path)
    if created:
        print("Repository created with success!")


if __name__ == "__main__":
    cli = CLI()
    tokenManager = TokenManager()
    token = tokenManager.readToken()
    cli.authenticate(token, logs=False)
    main.add_command(authenticate)
    main.add_command(template)
    main.add_command(create)
    main()
