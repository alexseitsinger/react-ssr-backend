import click
from subprocess import Popen


YARN_RUN_ARGS = ["yarn", "run"]
SSD_ARGS = YARN_RUN_ARGS + ["start:server:development"]


@click.command()
def start():
    pass
    #p1 = Popen(SSD_ARGS)
    #p1.wait()
