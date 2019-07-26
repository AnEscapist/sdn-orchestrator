import docker
import os
import requests
from ucpe.docker_controller.docker_global import dcli, api_cli, sftp, ip, username
from ucpe.docker_controller.docker_controller_message import *

#======================docker images==========================

def list_images(name=None, all=True):
    func = list_images
    try:
        image_list = dcli.images.list(name=name, all=all)
        return image_list_message(list=image_list, name=name, all=all, func=func)
    except OSError as ose:
        return ose_error(ose, func)


def images_info(path='ImagesInfo.json', name=None, all=True):
    func = images_info
    imageInfo = {}
    imageInfo['Images'] = []
    if name:
        all = False
    try:
        image_list = dcli.images.list(name=name, all=all)
    except OSError as ose:
        return ose_error(ose, func)

    if os.path.exists(path):
        os.remove(path)
    for i in range(len(image_list)):
        imageInfo['Images'].append(image_list[i].attrs)
        # return images_info_message(imageInfo, func)
    json_str = json.dumps(imageInfo, indent=4)
    try:
        with open(path, 'a') as json_file:
            json_file.write(json_str)
    except FileNotFoundError:
        return fnf_error(path, func)
    # return json_file_message(path, func)
    return images_info_message(imageInfo, path, func)

def inspect_image(name):
    func = inspect_image
    try:
        inspection = api_cli.inspect_image(name)
    except docker.errors.APIError as ae:
        return api_error(ae, func)

    return inspect_image_message(name, inspection, func)


def save_image(image_name, local_path, remote_path, local_save=False, chunk_size=2097152):
    func = save_image
    try:
        remote_file = sftp.open(remote_path, 'wb')
    except FileNotFoundError:
        remote_path = f'{username}@{ip}:{remote_path}'
        return fnf_error(remote_path, func)
    image = dcli.images.get(image_name)
    generator = image.save(chunk_size=chunk_size, named=image.tags)
    for chunk in generator:
        remote_file.write(chunk)
    remote_file.close()
    if local_save:
        #sftp.get(remotePath, localPath)
        os.system(f'rsync {username}@{ip}:{remote_path} {local_path}')
    return save_image_message(image_name, local_path, username,
                                  ip, remote_path, local_save, func)
        #os.system('rsync potato@10.10.81.100:/tmp/remote-image.tar /tmp/local-image.tar')


def create_image(remote_path):
    func = create_image
    try:
        with sftp.open(remote_path, 'rb') as f:
            image = dcli.images.load(data=f)
            remote_path = f'{username}@{ip}:{remote_path}'
            return create_image_message(image[0].id, remote_path, func)
    except TypeError as te:
        return type_error(te, func)
    except docker.errors.ImageLoadError:
        remote_path = f'{username}@{ip}:{remote_path}'
        return il_error(remote_path, func)
    except FileNotFoundError:
        return fnf_error(remote_path, func)


def pull_image(repo, registry, tag=None):
    print('=====================', registry)
    func = pull_image
    if registry == 'docker hub':
        try:
            dcli.images.pull(repository=repo, tag=tag)
            return pull_image_message(repo, tag, registry, func)
        except TypeError as te:
            return type_error(te, func)
        except requests.exceptions.HTTPError as re:
            return pull_error(re, func)
    else:
        if tag == None:
            try:
                os.system('docker pull ' + registry + '/' + name)
                return pull_image_message(repo, tag, registry, func)
            except TypeError as te:
                return type_error(te, func)
            except requests.exceptions.HTTPError as re:
                return pull_error(re, func)
        else:
            try:
                os.system('docker pull ' + registry + '/' + name + ':' + tag)
                return pull_image_message(repo, tag, registry, func)
            except TypeError as te:
                return type_error(te, func)
            except requests.exceptions.HTTPError as re:
                return pull_error(re, func)

        # else:
        #     try:
        #         os.system('docker pull ' + registry + '/' + name + ':' + tag)
        #         return pull_image_message(repo, tag, registry, func)


def remove_image(name):
    func = remove_image
    try:
        dcli.images.remove(name)
    except docker.errors.APIError as ae:
        return api_error(ae, func)
    return remove_image_message(name, func)

#=======================docker images end======================================
