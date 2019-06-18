import pytest
import subprocess
import ucpe.libvirt.utils as utils

def test_connect():
    utils.connect()

def test_read():
    #TODO: replace with relative path
    utils.read("/home/attadmin/projects/sdn-orchestrator/ucpe/agent-vm/ubuntu.xml")
