# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
import json
import urllib
import urllib2
from serverxmpp import ServerXmppBot

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
    return "hello world"


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
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

def put():
    vars = request.get_vars
    xids = vars['xmppid'].split(" ")
    xidp = vars['xmpppw'].split(" ")
    nodeip = vars['nodeip'].split(" ")
    xidh = vars['xmpphost'].split(" ")
    for i in range(len(xids)):
        db.xmpnode.insert(jid=xids[i],password=xidp[i],ip=nodeip[i],xmpp_host=xidh[i],vpn_name='sushant')
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
        return 'alice_sushant@xmpp.jp'

def set():
    vars = request.get_vars
    db(db.xmpnode.jid == vars['xmppid']).update(public_key=vars['public_key'])

def xmppbotCB(client, msg):
    values = {'xmppid' : client,'public_key':msg}
    data = urllib.urlencode(values)
    a = urllib2.urlopen('http://127.0.0.1:8000/IPOP/default/set?'+data)
    print 'http://127.0.0.1:8000/IPOP/default/set?'+data
    return


def xmppbot():
    #change this to make it more general ask user to enter xmpp jid and pass
    serverxmpp = ServerXmppBot('alice_sushant@xmpp.jp', 'alice123')
    serverxmpp.connect()
    serverxmpp.process(block=False)
    serverxmpp.add_callback('on_key_recvd',xmppbotCB)

def call():
    return service()
