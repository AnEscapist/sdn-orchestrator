import click
import ucpe.docker_commands.container_commands as ct_comm
import ucpe.docker_commands.image_commands as img_comm
import ucpe.docker_commands.network_commands as net_comm

@click.group()
def docker():
    '''
    docker commands.
    '''

docker.add_command(ct_comm.container)
docker.add_command(img_comm.image)
docker.add_command(net_comm.network)