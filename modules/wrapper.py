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
        args = ['timeout', '3s', './create_room.py']#, '-r', 'config.ini']
        p = subprocess.Popen(args)
        print p.wait()
        print p.communicate()
        pass

    def set_create_room_config(self, config):
        pass
awr = AdminGVPNWrapper()
awr.create_room('a@ejab', 'pass', '192.168.0.1', 'sushant')
