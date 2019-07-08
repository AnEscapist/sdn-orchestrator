import click
import ucpe.docker_controller.docker_controller_container as dcc



@click.group()
def container():
    '''
    docker container commands.
    '''


@container.command()
@click.option('-a/-r', default=True, help='list all containers [-a] or running containers [-r].')
def list(a):
    '''
    list all containers (default) or running containers.
    '''
    click.echo(dcc.list_containers(all=a))


@container.command()
@click.option('-p', default='ContainerStatus.json', help='path to save the json file.')
@click.option('-a/-c', default=True, help='all containers [-a] or a certain container [-c].')
@click.option('-i', default=None, help='id or name of a certain container.')
def status(p, a, i):
    '''
    get status of a container(s) and save it to a json file.
    '''
    click.echo(dcc.containers_status(path=p, all=a, id_name=i))

@container.command()
@click.option('-p', default='ContainerInfo.json', help='path to save the json file.')
@click.option('-a/-r', default=True, help='all containers [-a] or running container [-r].')

def info(p, a):
    '''
    save info of all containers to a json file.
    '''
    click.echo(dcc.containers_info(path=p, all=a))

@container.command()
@click.option('-i', default=None, help='id or name of a certain container.')

def inspect(i):
    '''
    inspect a certain container.
    '''
    click.echo(dcc.inspect_container(id_name=i))


@container.command()
@click.option('-i', default=None, help='id or name of the container.')
@click.option('-r', default=None, help='the repository to push the image to.')
@click.option('-t', default=None, help='tag of the image.')
@click.option('-m', default=None, help='a commit message.')
@click.option('-a', default=None, help='the name of the author.')
@click.option('-c', default=None, help='dockerfile instructions to apply while committing.')

def commit(i, r, t, m, a, c):
    '''
    commit a container to an image.
    '''
    click.echo(dcc.commit(id_name=i, repo=r, tag=t, message=m, author=a, changes=c))


@container.command()
@click.option('-i', default=None, help='id or name of the container.')
@click.option('-l', default=None, help='local path to save the tar archive.')
@click.option('-r', default=None, help='remote path to save the tar archive.')
@click.option('-s/-u', default=False, help='save the tar archive locally [-s] or not [-u].')
def export(i, l, r, s):
    '''
    export the contents of the container's filesystem as a tar archive.
    '''
    click.echo(dcc.export_container(id_name=i, local_path=l, remote_path=r, local_save=s))


@container.command()
@click.option('-i', default=None, help='id or name of the image.')
@click.option('-p', default=None, help='ports to bind inside the container.' +
                                    ' Valid format: "container:host"' +
                                    ' e.g.: "2222/tcp:3333"'
                                    ', "2222/tcp:None"' +
                                    ', "1111/tcp:(127.0.0.1, 111)"' +
                                    ' or "1111/tcp:[1234, 4567]" '
                )
@click.option('-v', default=None, help='configure volumes mounted inside the container.' + '\n' +
                                        '{key1:{value1},key2:{value2}}' + '\n' +
                                        'key: host path or a volume name' + '\n' +
                                        'value: a dictionary with keys: ' + '\n' +
                                        '   bind: path to mount the volume inside the container' + '\n' +
                                        '   mode: "rw"-read/write, or "ro"-read only' + '\n' +
                                        'e.g. "{"my-vol": {"bind": "/mnt/vol2", "mode": "rw"}}"'
                                        )
def create(i, p, v):
    '''
    create a container using an image and start it.
    '''
    click.echo(dcc.create_container(image_name=i, ports=p, volumes=v))


@container.command()
@click.option('-i', default=None, help='id or name of the container.')
@click.option('-c', default=None, help='status to change [valid: running, exited, paused, restart].')
def change(i, c):
    '''
    change the status of a container
    '''
    click.echo(dcc.change_status(id_name=i, change_to=c))
