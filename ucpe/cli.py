import click
import ucpe.docker_controller.docker_controller as d_con
import ucpe.docker_commands.commands as d_commands
#from ucpe.docker.docker_controller import *

@click.group()
def start():
    """this is start"""


start.add_command(d_commands.docker)

