import click
import ucpe.docker_controller.docker_controller as dc_con
import ucpe.docker_commands.commands as dc_com
#from ucpe.docker.docker_controller import *

@click.group()
def start():
    '''
    docker commands start here.
    '''


start.add_command(dc_com.docker)

