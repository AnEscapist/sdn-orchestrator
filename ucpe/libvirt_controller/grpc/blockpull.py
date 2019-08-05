import subprocess

def blockpull(vm_name, save_path, base_path):
    '''
    calls the following bash command:
    virsh blockpull --domain vm_name --path save_path --base base_path --wait
                    --verbose
    pulls the backing chain from (base_path, save_path] into save_path
    :param vm_name: name of domain to perform blockpull operation on
    :param save_path: path to some image in backing chain
    :param base_path: path to image in backing chain which becomes the new base
    :return: result of above bash call

    example:
        backing chain for vm_test on ucpe U1:
            base <-- snap1 <-- snap2
        _blockpull(U1, vm_test, <snap2_path>, <base path>) would result in the backing chain
        base <-- snap2, where snap2 now also contains the data of snap1
    '''
    p = subprocess.Popen(["virsh", "blockpull", "--domain", vm_name, "--path", save_path, "--base", base_path, "--wait",
                    "--verbose"], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = p.communicate()
    return out,err

