# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
import json
import urllib
import urllib2
import serverxmpp
import gvpnconfig
import heartbeat
import admingvpnwrapper

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
    return dict()

def login():
    form=FORM('Login:', BR(),INPUT(_name='name',_placeholder='Admin name',requires=IS_IN_DB(db,db.users.username)),BR(),
        INPUT(_name='password',_type='password',_placeholder='Password',requires=IS_IN_DB(db,db.users.password)),BR(),
        INPUT(_type='submit',_value='login'))
    message = ''
    #form = SQLFORM(db.users)
    if form.validate():
        session.logged_in_user = form.vars.name
        redirect(URL(index))
    elif form.errors:
        form.errors.clear()
        message = "Please enter a valid username"
        session.logged_in_user = None # not necessary, but oh well
        response.flash  = "Please enter a valid username"
    return dict(form=form,message=message)

def user():
    return dict(form=auth())

@cache.action()
def download():
    return response.download(request, db)


def monitor():
    vars = request.get_vars
    jid = vars['xmppid']
    time_period = vars['duration'] or 'hour'
    query = db(db.xmpnode.jid == jid).select()
    if len(query) == 0:
        return "monitoring info not available"
    ip = query[0].ip

    ganglia_graph_params = {
        'z':'medium',
        'c':'my cluster',
        'r': time_period
        }
    info = [
        ['peer_conn_age_-'+ip,'Seconds','Connection age of '+ip],
        ['peer_bytes_recv_-'+ip,'Bytes/Seconds','Bytes recvd by '+ip],
        ['peer_bytes_sent_-'+ip,'Bytes/Seconds','Bytes sent by '+ip],
        ['peer_status_-'+ip,'On/Off','Status On/off of '+ip],
        ['peer_xmpp_time_-'+ip,'Seconds','Xmpp time of '+ip]
    ]
    #http://localhost/ganglia/graph.php?r=hour&z=medium&c=my+cluster&m=peer_bytes_recv_-192.170.32.3&vl=Bytes%2FSecond&ti=Bytes+received+by+192.170.32.3
    json_data = []
    for each_info in info:
        arr = {}
        ganglia_graph_params['m']=each_info[0]
        ganglia_graph_params['vl']=each_info[1]
        arr['title'] = ganglia_graph_params['ti']=each_info[2]
        arr['url'] = 'http://localhost/ganglia/graph.php?'+urllib.urlencode(ganglia_graph_params)
        json_data.append(arr)

    return dict(json = json_data)

def creategvpn():
    return dict()

def editgvpn():
    json = {}
    j = 0
    for row_vpn in db(db.vpn).select():
        j+=1
        json_vpn = {}
        json_vpn['vpn_id'] = row_vpn.id
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
    id = db.vpn.insert(vpn_name=vars['vpnname'],description="none",admin_jid=vars['adminjid'],admin_password=vars['adminpw'],ipv4_mask=vars['subnet'],ejabberd_password=vars['xmpp_host_password'])
    xids = vars['xmppid'].split(" ")
    xidp = vars['xmpppw'].split(" ")
    nodeip = vars['nodeip'].split(" ")
    xidh = vars['xmpphost'].split(" ")
    for i in range(len(xids)):
        db.xmpnode.insert(jid=xids[i],password=xidp[i],ip=nodeip[i],xmpp_host=xidh[i],status="stopped",vpn_id=id)
    return dict(request.get_vars)

def delet():
    vars = request.get_vars
    jids = vars['jids'].split()
    for jid in jids:
        data = {}
        query_result = db(db.xmpnode.jid == jid).select()
        if len(query_result) == 0:
            return dict(json={'return_code':2,'msg':'Node '+jid+' doesn\'t exist in db'})
        ejabberd_password = db(db.vpn.id == query_result[0].vpn_id).select()[0].ejabberd_password
        data['jid'] = jid
        data['xmpp_host'] = query_result[0].xmpp_host
        #if ejabberd_password is empty, implies non-ejabberd server
        if ejabberd_password != '':
            data['xmpp_host_password'] = ejabberd_password
            response = urllib2.urlopen('http://127.0.0.1:8000%s?%s'%(URL('unregister_relationship.json'),urllib.urlencode(data)))
            response = json.loads(response.read())
            if response['json']['return_code'] == 2:
                #if its non-ejabberd server,ignore
                if response['json']['msg'] != "The ipop-ejabberd server is not running":
                    return dict(json=response['json'])
        db(db.xmpnode.jid == jid).delete()
    return dict(json={'return_code':0,'msg':'successfully deleted'})


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

#handles multiple ejabberd node insert and response
def register_relationships():
    vars = request.get_vars
    response_ob = {}
    xmpp_host,xmpp_host_password,no_of_nodes,vpn_name,ip,ipv4mask = vars['xmpp_host'],vars['xmpp_host_password'],vars['no_of_nodes'], vars['vpnname'], vars['ip4'], vars['subnet']
    for ele in [xmpp_host,no_of_nodes,vpn_name,ip,ipv4mask,xmpp_host_password]:
        if not ele :
            response_ob['return_code'] = 2
            response_ob['msg'] = 'Some arguments were not passed'
            return dict(json =response_ob)
    try:
        instructions,config = gvpnconfig.getConfScript(ip,ipv4mask,vpn_name,xmpp_host,no_of_nodes)
    except OSError as er:
        response_ob['return_code'] = 2
        response_ob['msg'] = str(er)
        return dict(json =response_ob)
    for each_config in config:
        ip_match = db(db.xmpnode.ip == each_config['ip4'] ).select()
        if len(ip_match)>0:
            response_ob['return_code'] = 2
            response_ob['msg'] = "The IP "+ip_match[0]['ip']+" is already engaged in the db"
            return dict(json =response_ob)
    try:
        resp = gvpnconfig.send_ejabberd(xmpp_host,instructions,xmpp_host_password)
    except OSError as er:
        response_ob['return_code'] = 2
        response_ob['msg'] = str(er)
        return dict(json =response_ob)

    #FIX-THIS = dependent on front end
    node_list = []
    for each_config in config:
        node = {}
        node['xmpp_username'] = each_config['xmpp_username']
        node['xmpp_password'] = each_config['xmpp_password']
        node['xmpp_host'] = vars['xmpp_host']
        node['ip4'] = each_config['ip4']
        node_list.append(node)

    resp = json.loads(resp)
    resp['nodes'] = node_list
    return dict(json=resp)


#handles single ejabberd node delete
def unregister_relationship():
    vars = request.get_vars
    jid = vars['jid']
    xmpp_host = vars['xmpp_host']
    xmpp_host_password = vars['xmpp_host_password']
    #user@ejabberd => user ejabberd
    instruction = "ejabberdctl unregister %s"%(jid.replace('@',' '))
    try:
        resp = gvpnconfig.send_ejabberd(xmpp_host,instruction,xmpp_host_password,delet = 1)
    except OSError as er:
        return dict(json={'return_code':2,'msg':str(er)})
    resp = json.loads(resp)
    return dict(json=resp)

def admingvpn():
    vars = request.get_vars
    admin_jid,admin_pw,xmpp_host,vpn_name,ipspace = vars['admin_jid'],vars['admin_password'],vars['xmpp_host'], vars['vpnname'], vars['ipspace'] 
    vpn_name = vpn_name.lower()
    if vars['type'] == 'create':
        # create muc room
        try:
            #admingvpnwrapper.create_room('agvpn@ejabberd','agvpn','127.0.0.1','susano')
            admingvpnwrapper.create_room(admin_jid,admin_pw,xmpp_host,vpn_name)
        except ValueError as er:
            return dict(json={'return_code':2,'msg':str(er)})
        return dict(json={'return_code':0,'msg':'success'})
    elif vars['type'] == 'invite' or vars['type'] == 'delete':
        #handle invite
        try:
            #admingvpnwrapper.set_config('agvpn@ejabberd','agvpn','127.0.0.1','susano','192.167.0.0',vars['jids'].split())
            admingvpnwrapper.set_config(admin_jid,admin_pw,xmpp_host,vpn_name,ipspace,vars['jids'].split())
            if vars['type'] == 'invite':
                ip_alloc = admingvpnwrapper.invite()
                return dict(json={'return_code':0,'msg':ip_alloc })
            elif vars['type'] == 'delete':
                admingvpnwrapper.delete()
        except ValueError as er:
            return dict(json={'return_code':2,'msg':str(er)})
        return dict(json={'return_code':0,'msg':'success'})
    elif vars['type'] == 'destroy':
        #deletes room completely
        try:
            admingvpnwrapper.delete_room(vpn_name)
        except OSError as er:
            return dict(json={'return_code':2,'msg':'room doesn\'t exist'})
        return dict(json={'return_code':0,'msg':'success'})
    return dict()

def getgraph():
    vars = request.get_vars
    if len(vars) == 0:
        return dict()
    #get nodes in the vpn
    vid = vars['vpnid']
    vpn_nodes= db(db.xmpnode.vpn_id == vid).select()
    #get all xmpp hosts
    xmpphostarray = []
    for node in vpn_nodes:
        if node.xmpp_host not in xmpphostarray:
            xmpphostarray.append(node.xmpp_host)
    #set up node and Links
    Nodes = []
    Links = []
    for xh in xmpphostarray:
        each_node = {}
        each_node['name']=xh
        each_node['password']=''
        each_node['ip']=''
        each_node['group']=0
        Nodes.append(each_node)
    for node in vpn_nodes:
        each_node = {}
        each_link = {}
        each_node['name']=node.jid
        each_node['password']=node.password
        each_node['ip']=node.ip
        if node.status == 'running':
            each_node['group']=1 # green color
        else:
            each_node['group']=2 # red color

        each_link["source"]=len(Nodes)
        each_link["target"]=xmpphostarray.index(node.xmpp_host)
        Nodes.append(each_node)
        Links.append(each_link)
    json = {}
    json["nodes"]=Nodes
    json["links"]=Links
    return json

def log():
    vars = request.get_vars
    if vars['type'] == 'set':
        select_list = db((db.logs.node == vars['node'])&(db.logs.name == vars['name'])).select()
        if len(select_list) ==0:
            db.logs.insert(node = vars['node'], name = vars['name'],log = vars['log'])
        else:
            existing_log = select_list[0]['log']
            db((db.logs.node == vars['node'])&(db.logs.name == vars['name'])).update(log = vars['log'] + existing_log)
        return 'success'
    elif vars['type'] == 'del':
        pass
    else:
        select_list = db(db.logs.node == vars['node']).select()
        if len(select_list) ==0:
            return dict(json ='')
        else:
            if vars['name']:
                for entry in select_list:
                    if entry.name == vars['name']:
                        return dict(json = [entry])
                return dict(json = '')
        return dict(json = select_list)


def set():
    vars = request.get_vars
    if(vars['type'] == 'set_public_key'):
        db(db.xmpnode.jid == vars['xmppid']).update(public_key=vars['public_key'])
    elif(vars['type'] == 'change_status'):
        if vars['status'] == 'running':
            heartbeat.beat(vars['xmppid'])
        elif vars['status'] == 'stopped':
            heartbeat.kill(vars['xmppid'])
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


def call():
    return service()
