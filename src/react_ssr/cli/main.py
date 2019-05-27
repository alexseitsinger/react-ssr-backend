import click

from .commands.start import start


@click.group()
def main():
    pass


main.add_command(start)
