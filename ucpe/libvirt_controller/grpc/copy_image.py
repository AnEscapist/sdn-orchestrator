import subprocess
import os

BASE_DIRECTORY = '/var/third-party/base'
ACTIVE_DIRECTORY = '/var/third-party/active'
def copy_image(vm_name, image_file_name):
    base_path = os.path.join(BASE_DIRECTORY, image_file_name)
    image_active_dir = os.path.join(ACTIVE_DIRECTORY, vm_name)
    os.makedirs(image_active_dir, exist_ok=True) #todo: exist_ok=true is REALLY BAD.  unsafe. doesn't fail fast.  rethink this.
    p = subprocess.Popen(['cp', base_path, image_active_dir], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = p.communicate()
    return out, err

if __name__ == '__main__':
    vm_name = 'test'
    image_file_name = 'storage.qcow2'
    copy_image(vm_name, image_file_name)

