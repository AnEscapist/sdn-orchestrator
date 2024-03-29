def show_active_ports(child):
    child.sendline('ports')
    child.expect('BCM.0>')
    raw = child.before.decode('utf-8')
    lines = raw.split('\n')
    output = ''
    for line in lines[3:-1]:
        words = line.split()
        output += words[0] + words[1] + ' ' + words[2] + '\n'
    return output


def show_vlans(child):
    child.sendline('vlan show')
    child.expect('BCM.0>')
    return child.before.decode('utf-8')


def create_vlan(child, vlanid):
    command = 'vlan create ' + str(vlanid)
    child.sendline(command)
    child.expect('BCM.0>')
    print(child.before.decode('utf-8'))


def add_ports(child, vlanid, pbm, ubm):
    command = 'vlan add ' + str(vlanid) + ' pbm=' + str(pbm)
    if ubm != '':
        command = command + ' ubm=' + str(ubm)
    child.sendline(command)
    child.expect('BCM.0>')
    print(child.before.decode('utf-8'))


def rem_ports(child, vlanid, pbm):
    command = 'vlan remove ' + str(vlanid) + ' pbm=' + str(pbm)
    child.sendline(command)
    child.expect('BCM.0>')
    print(child.before.decode('utf-8'))


def destroy_vlan(child, vlanid):
    command = 'vlan destroy ' + str(vlanid)
    child.sendline(command)
    child.expect('BCM.0>')
    print(child.before.decode('utf-8'))


def set_pvlan(child, port, vlanid):
    command = 'pvlan set ' + str(port) + ' ' + str(vlanid)
    child.sendline(command)
    child.expect('BCM.0>')
    print(child.before.decode('utf-8'))


def show_pvlans(child):
    child.sendline('pvlan show')
    child.expect('BCM.0>')
    return child.before.decode('utf-8')
