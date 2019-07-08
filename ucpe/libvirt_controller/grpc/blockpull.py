import subprocess

def blockpull(vm_name, save_path, base_path):
    subprocess.run(["virsh", "blockpull", "--domain", vm_name, "--path", save_path, "--base", base_path, "--wait",
                    "--verbose"])

