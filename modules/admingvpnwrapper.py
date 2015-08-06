import subprocess
import os
import shutil

#FIX-THIS
DIR = os.getcwd()+'/applications/IPOP/static/scripts/'
CWD = DIR

# assumes duplicate validation already done
def create_room(adminjid, password, xmpphost, vpnname):
    # set config file
    with open(DIR+'room_config.ini', 'r') as f:
        room_config = f.read()
        with open(DIR+'config.ini', 'w') as fo:
            fo.write(room_config % (adminjid, password, xmpphost, vpnname))
    # run create_room
    args = ['timeout', '8s', 'python', DIR+'create_room.py',
            '-r', DIR+'config.ini']
    makeDir(vpnname)
    p = subprocess.Popen(args, cwd=CWD, stdout=subprocess.PIPE)
    if p.wait() != 0:
        raise ValueError('Error: while creating room')
        removeDir(vpnname)
    if 'Success' not in p.stdout.read():
        raise ValueError('Error: data in form incorrect')
        removeDir(vpnname)
    return 0

def manage_room(arg, arg_desc):
    # run manageuser
    args = ['timeout', '8s', 'python', DIR+'manageUsers.py', '-u',
            DIR+'config.ini',  arg, arg_desc]
    p = subprocess.Popen(args, cwd=CWD, stdout=subprocess.PIPE)
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

def delete_room(vpnname):
    removeDir(vpnname)

def delete():
    return manage_room('-d', 'DELETE')

def invite():
    return manage_room('-i', 'INVITE')

def makeDir(vpnname):
    global CWD
    if not os.path.exists(DIR+'db/'+vpnname+'/'):
        os.makedirs(DIR+'db/'+vpnname+'/')
    CWD = DIR+'db/'+vpnname+'/'

def removeDir(vpnname):
    global CWD
    CWD = DIR+'db/'+vpnname+'/'
    shutil.rmtree(CWD)
    
def set_config(adminjid, password, xmpphost, vpnname, ipspace,
               jids=[]):
    if len(jids) == 0:
        raise ValueError('Jids not passed')
    jid_string = " : None\n".join(jids) + " : None"
    # open applicants.ini
    with open(DIR+'applicants.ini', 'r') as f:
        with open(DIR+'config.ini', 'w') as fo:
            fo.write(f.read() % (xmpphost, adminjid, password, vpnname,
                                 ipspace, jid_string))
    makeDir(vpnname)
#print open('../static/scripts/room_config.ini').read()
#awr = AdminGVPNWrapper()
#awr.create_room('agv@ejabberd', 'agvpn', '127.0.0.1', 'sushant')
#awr.set_config('agv@ejabberd', 'agvpn', '127.0.0.1', 'sushant',
# '192.166.0.0', ['sus','tt','bok'])
#print awr.invite()
