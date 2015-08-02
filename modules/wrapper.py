import subprocess


class AdminGVPNWrapper:
    def __init__(self):
        print subprocess.check_output(['./create_room.py'])

    def create_room(self, adminjid, password, xmpphost, vpnname):
        # set config file
        with open('room_config.ini', 'r') as f:
            room_config = f.read()
            with open('config.ini', 'w') as fo:
                fo.write(room_config % (adminjid, password, xmpphost, vpnname))
        # run create_room
        args = ['timeout', '8s', './create_room.py', '-r', 'config.ini']
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        if p.wait() != 0:
            raise ValueError('Error: while creating room')
        if 'Success' not in p.stdout.read():
            raise ValueError('Error: data in form incorrect')
        return 0

awr = AdminGVPNWrapper()
awr.create_room('agv@ejabberd', 'agvpn', '127.0.0.1', 'sushant')
