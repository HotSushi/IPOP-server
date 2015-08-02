import subprocess


class AdminGVPNWrapper:
    DIR = '../static/scripts/'

    def __init__(self):
        pass

    def create_room(self, adminjid, password, xmpphost, vpnname):
        # set config file
        with open(self.DIR+'room_config.ini', 'r') as f:
            room_config = f.read()
            with open(self.DIR+'config.ini', 'w') as fo:
                fo.write(room_config % (adminjid, password, xmpphost, vpnname))
        # run create_room
        args = ['timeout', '8s', 'python', self.DIR+'create_room.py',
                '-r', self.DIR+'config.ini']
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        if p.wait() != 0:
            raise ValueError('Error: while creating room')
        if 'Success' not in p.stdout.read():
            raise ValueError('Error: data in form incorrect')
        return 0

    def manage_room(self, arg, arg_desc):
        # run manageuser
        args = ['timeout', '8s', 'python', self.DIR+'manageUsers.py', '-u',
                self.DIR+'config.ini',  arg, arg_desc]
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        if p.wait() != 0:
            raise ValueError('Error: while managing room')
        # if invite type extract ip allocation
        if arg == '-i':
            ip_alloc = {}
            lines = p.stdout.read().split('\n')
            for line in lines[2:]:
                if '::' in line:
                    jid, ip = line.split('::')
                    ip_alloc[jid] = ip
            return ip_alloc
        return 0

    def delete(self):
        return self.manage_room('-d', 'DELETE')

    def invite(self):
        return self.manage_room('-i', 'INVITE')

    def set_config(self, adminjid, password, xmpphost, vpnname, ipspace,
                   jids=[]):
        if len(jids) == 0:
            raise ValueError('Jids not passed')
        jid_string = " : None\n".join(jids) + " : None"
        # open applicants.ini
        with open(self.DIR+'applicants.ini', 'r') as f:
            with open(self.DIR+'config.ini', 'w') as fo:
                fo.write(f.read() % (xmpphost, adminjid, password, vpnname,
                                     ipspace, jid_string))

#print open('../static/scripts/room_config.ini').read()
#awr = AdminGVPNWrapper()
#awr.create_room('agv@ejabberd', 'agvpn', '127.0.0.1', 'sushant')
#awr.set_config('agv@ejabberd', 'agvpn', '127.0.0.1', 'sushant',
# '192.166.0.0', ['sus','tt','bok'])
#print awr.invite()
