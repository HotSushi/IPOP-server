# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
import json
import urllib
import urllib2
import serverxmpp

from Crypto.PublicKey import RSA

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #Have to create LOGIN
    serverxmpp.init()
    #serverxmpp.instance.add_callback('on_key_recvd',xmppbotCB)
    return dict()


def user():
    return dict(form=auth())


@cache.action()
def download():
    return response.download(request, db)


def monitor():
    #fix-this
    f = open("/home/hotsushi/ipopstats/peer_list_ganglia.json")
    peers = []
    for line in f:
        data = json.loads(line)
        peers.append(data[0])
    return dict(peerlist = peers)

def creategvpn():
    return dict()

def editgvpn():
    json = {}
    j = 0
    for row_vpn in db(db.vpn).select():
        j+=1
        json_vpn = {}
        json_vpn['vpn_name'] = row_vpn.vpn_name
        json_vpn['vpn_description'] = row_vpn.description
        json_vpn['vpn_admin'] = row_vpn.admin_jid
        json_vpn['vpn_password'] = row_vpn.admin_password
        json_vpn['vpn_ipv4mask'] = row_vpn.ipv4_mask
        json_node = {}
        i = 0
        for row in db(db.xmpnode).select():
            if row.vpn_id == row_vpn.id:
                i += 1
                dic = {}
                dic['jid'] = row.jid
                dic['password'] = row.password
                dic['xmpp_host'] = row.xmpp_host
                dic['ip'] = row.ip
                dic['status'] = row.status
                json_node[i] = dic
        json_vpn['nodes'] = json_node
        json[j]=json_vpn
    return dict(json = json)

def put():
    vars = request.get_vars
    id = db.vpn.insert(vpn_name=vars['vpnname'],description="none",admin_jid=vars['adminjid'],admin_password=vars['adminpw'],ipv4_mask=vars['subnet'])
    xids = vars['xmppid'].split(" ")
    xidp = vars['xmpppw'].split(" ")
    nodeip = vars['nodeip'].split(" ")
    xidh = vars['xmpphost'].split(" ")
    for i in range(len(xids)):
        db.xmpnode.insert(jid=xids[i],password=xidp[i],ip=nodeip[i],xmpp_host=xidh[i],status="stopped",vpn_id=id)
    return dict(request.get_vars)

def get():
    vars = request.get_vars
    if len(vars) == 0:
        return dict()
    if vars['type'] == 'getjson':
        xid = vars['xmppid']
        row = db(db.xmpnode.jid == xid).select()[0]
        dic = {
            "xmpp_username": "",
            "xmpp_password": "",
            "xmpp_host": "",
            "ip4": "",
            "ip4_mask": 24,
            "stat_report": True,
            "tincan_logging": 0,
            "controller_logging": "DEBUG"
            }
        dic['xmpp_username'] = row.jid
        dic['xmpp_password'] = row.password
        dic['xmpp_host'] = row.xmpp_host
        dic['ip4'] = row.ip
        config = json.dumps(dic)
        key = RSA.importKey(row.public_key)
        enc_data = key.encrypt(config, 32)[0]
        return enc_data
    elif vars['type'] == 'getserverjid':
        xid = vars['xmppid']
        vid = db(db.xmpnode.jid == xid).select()[0].vpn_id
        adminxmpp = db.vpn[vid].admin_jid
        return adminxmpp

def set():
    vars = request.get_vars
    if(vars['type'] == 'set_public_key'):
        db(db.xmpnode.jid == vars['xmppid']).update(public_key=vars['public_key'])
    elif(vars['type'] == 'change_status'):
        db(db.xmpnode.jid == vars['xmppid']).update(status=vars['status'])
    elif(vars['type'] == 'change_ip'):
        db(db.xmpnode.jid == vars['xmppid']).update(ip=vars['ip'])

def sendtoclient():
    vars = request.get_vars
    #fix-this: a xmppid may have 2 or more admins (fix: pass vpn_id also)
    #switch to respective admin
    vid = db(db.xmpnode.jid == vars['xmppid']).select()[0].vpn_id
    admin_jid,admin_password = db.vpn[vid].admin_jid,db.vpn[vid].admin_password
    serverxmpp.change_instance(admin_jid,admin_password)
    if vars['type'] == 'stop':
        serverxmpp.instance.stop_client(vars['xmppid'])
    elif vars['type'] == 'change_ip':
        serverxmpp.instance.change_ip(vars['xmppid'])
    elif vars['type'] == 'received_ack':
        serverxmpp.instance.send_key_ack(vars['xmppid'])


def xmppbotCB(client, msg):
    values = {'type':'set_public_key','xmppid' : client,'public_key':msg}
    data = urllib.urlencode(values)
    #cannot access from non-web2py thread
    a = urllib2.urlopen('http://localhost:8000/IPOP/default/set?'+data)
    #print 'http://127.0.0.1:8000/IPOP/default/set?'+data
    return

def call():
    return service()
