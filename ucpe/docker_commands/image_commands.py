import click
import ucpe.docker_controller.docker_controller_image as dci



@click.group()
def image():
    '''
    docker image commands.
    '''


@image.command()
@click.option('-a/-f', default=True, help='list all images [-a] or filter out intermediate image layers. [-f].')
@click.option('-n', default=None, help='only show images belonging to the repository name.')
def list(a, n):
    '''
    list all images (default) or images belonging to a repository.
    '''
    click.echo(dci.list_images(name=n, all=a))


@image.command()
@click.option('-p', default='ImageInfo.json', help='path to save the json file')
@click.option('-n', default=None, help='only show the info of images belonging to the repository name.')
@click.option('-a/-f', default=True, help='show the info of all images [-a] or filter out intermediate image layers. [-f].')
def info(p, n, a):
	'''
	save info of images to a json file.
	'''
	click.echo(dci.images_info(path=p, name=n, all=a))


@image.command()
@click.option('-n', default=None, help='name of the image.')
@click.option('-l', default=None, help='local path to save the tar archive.')
@click.option('-r', default=None, help='remote path to save the tar archive.')
@click.option('-s/-u', default=False, help='save the tar archive locally [-s] or not [-u].')
def save(n, l, r, s):
	'''
	save an image to a tar archive.
	'''
	click.echo(dci.save_image(image_name=n, local_path=l, remote_path=r, local_save=s))

@image.command()
@click.option('-p', default=None, help='path to create the image.')
def create(p):
	'''
	create an image that was previously saved using 'save' (or docker save).
	'''
	click.echo(dci.create_image(remote_path=p))

@image.command()
@click.option('-r', default=None, help='the repository to pull')
@click.option('-t', default=None, help='the tag to pull')
def pull(r, t):
	'''
	pull an image of the given name and return it.
	'''
	click.echo(dci.pull_image(repo=r, tag=t))