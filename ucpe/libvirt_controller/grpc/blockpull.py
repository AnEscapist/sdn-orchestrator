import subprocess

def blockpull(vm_name, save_path, base_path):
    p = subprocess.Popen(["virsh", "blockpull", "--domain", vm_name, "--path", save_path, "--base", base_path, "--wait",
                    "--verbose"], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = p.communicate()
    return out,err


