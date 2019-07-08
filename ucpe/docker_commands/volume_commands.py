import click
import ucpe.docker_controller.docker_controller_volume as dcv



@click.group()
def volume():
    '''
    docker volume commands.
    '''


@volume.command()
@click.option('-n', default=None, help='name of the new volume.')
def create(n):
    '''
    create a new volume.
    '''
    click.echo(dcv.create_volume(name=n))
