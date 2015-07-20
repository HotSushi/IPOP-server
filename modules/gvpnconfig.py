import subprocess
import json
import urllib
import urllib2

#throws OSError
def getConfScript(ip,ip4mask,name,ejabberd_ip,no_of_nodes):
    #fix-this = 'is ejabberd_ip necessary'
    if no_of_nodes == 0:
        return ''
    ipplusmask = ip+'/'+ip4mask
    args = ['groupvpn-config','--ip-network',ipplusmask,name,'ejabberd',no_of_nodes]
    try:
        result = subprocess.check_output(args, stderr=subprocess.STDOUT)
    except OSError as e:
        raise OSError('groupvpn-config not installed correctly') 
    except:
        raise OSError('IP space should end with 0, for ex 192.168.2.0')       
    return process(result)

def process(result):
    i = result.find('{')
    return [result[:i],getConfJsonFromString(result[i:])]   

def getConfJsonFromString(blob):
    AR = []
    next_cb = blob.find('}')
    while next_cb != -1:
        AR.append( json.loads(blob[:next_cb+1]) )
        blob =blob[next_cb+1:]
        next_cb = blob.find('}')
    return AR

def send_ejabberd(hostip,data,password,delet=0):
    values = {'cmd':data,'pw' : password}
    data = urllib.urlencode(values)
    try:
        if delet == 0:
            response = urllib2.urlopen('http://%s:7000/create.py?%s'%(hostip,data) , timeout = 3)
        elif delet == 1:
            response = urllib2.urlopen('http://%s:7000/delete.py?%s'%(hostip,data) , timeout = 3)
    except urllib2.HTTPError, e:
        raise OSError('There is some problem in the ipop-ejabberd server')
    except urllib2.URLError, e:
        raise OSError('The ipop-ejabberd server is not running')
    return response.read()



#t =  getConfScript('123.31.0.0','21','vpnname','145.3.2.1','2')
#print t
