import click
from ucpe.docker_controller.docker_controller import *

@click.group()
def docker():
    '''
    docker docker
    '''
    print('this is docker command')

@docker.command()
def restart():
    '''
    this is restart
    '''
    print(remove_network('01152bbaa74296e1468622c13c983b4fcebbe99bdcc1dac9f6ae8210e79b98a2'))

@docker.command()
def create():

    '''
    create create
    :return:
    '''