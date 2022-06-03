import click
from modules.clis import CLI

cli = None


@click.group(help="Automatically create GitHub repositories.")
def main() -> None:
    pass

# Set token.


@click.command(name="set-token")
@click.argument("access_token")
def setToken(access_token: str) -> bool:
    cli.setToken(access_token)

# Template.


@click.command(name="template")
@click.argument("template_type")
def template(template_type: str) -> bool:
    cli.template(template_type)

# Create.


@click.command(name="create")
@click.argument("absolute_file_path")
def create(absolute_file_path: str) -> bool:
    cli.create(absolute_file_path)


if __name__ == "__main__":
    cli = CLI()
    cli.authenticate("TOKEN")
    main.add_command(setToken)
    main.add_command(template)
    main.add_command(create)
    main()
