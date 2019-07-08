import subprocess

def blockpull(vm_name, save_path, base_path, verbose=True):
    subprocess.run(["virsh", "blockpull", "--domain", vm_name, "--path", save_path, "--base", base_path, "--wait",
                    "--verbose" if verbose else ""])


