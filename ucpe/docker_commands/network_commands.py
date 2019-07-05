import click
import ucpe.docker_controller.docker_controller_network as dcn



@click.group()
def network():
    '''
    docker network commands.
    '''


@network.command()
@click.option('-n', default=None, help='name of the network.')
@click.option('-d', default='bridge', help='name of the driver used to create the network, Default: [bridge].')
@click.option('-s', default=None, help='subnet of the network, e.g. [10.10.81.1/24].')
@click.option('-g', default=None, help='gateway of the network, e.g. [10.10.81.8].')
@click.option('-e/-u', default=False, help='enable ipv6 [-e] or not [-u].')
def create(n, d, s, g, e):
    '''
    create a network.
    '''
    click.echo(dcn.create_network(network_name=n, driver=d, subnet=s, gateway=g, enable_ipv6=e))

@network.command()
@click.option('-i', default=None, help='id or name of the container.')
@click.option('-n', default=None, help='name of the network.')

def connect(i, n):
	'''
	connect a container to this network.
	'''
	click.echo(dcn.connect_container(id_name=i, network_id=n))


@network.command()
@click.option('-i', default=None, help='id or name of the container.')
@click.option('-n', default=None, help='name of the network.')
@click.option('-u/-f', default=False, help='force the container to disconnect from a network. Default: false[-u].')

def disconnect(i, n, u):
	'''
	disconnect a container to this network.
	'''
	click.echo(dcn.disconnect_container(id_name=i, network_id=n, force=u))


@network.command()
@click.option('-n', default=None, help='name of the network.')

def remove(n):
	'''
	remove the network.
	'''
	click.echo(dcn.remove_network(network_id=n))


