import subprocess
import json

def getConfScript(ip,ip4mask,name,ejabberd_ip,no_of_nodes):
    if no_of_nodes == 0:
        return ''
    ipplusmask = ip+'/'+ip4mask
    args = ['groupvpn-config','--ip-network',ipplusmask,name,ejabberd_ip,no_of_nodes]
    result = subprocess.check_output(args, stderr=subprocess.STDOUT)
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

#t =  getConfScript('123.31.0.0','21','vpnname','145.3.2.1','2')
