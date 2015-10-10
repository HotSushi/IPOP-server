from threading import Timer
import urllib
import urllib2

running_timers = {}

PORT_NO = '8000'

def set_port_no(portno):
    global PORT_NO
    PORT_NO = str(portno)

def setJidStopped(jid, vpnname):
    kill(jid)
    data = urllib.urlencode({'type':'change_status','xmppid':jid,'vpnname':vpnname,'status':'stopped'})
    urllib2.urlopen('http://127.0.0.1:%s/IPOP/default/set?%s'%(PORT_NO,data))
    
#after 5 minutes the function will go off
def beat(jid, vpnname):
    if jid in running_timers:
        kill(jid)
    running_timers[jid] = Timer(10,setJidStopped, [jid, vpnname])
    running_timers[jid].start()

#timer stop  
def kill(jid):
    if jid not in running_timers:
        return
    running_timers[jid].cancel()
    del running_timers[jid]

'''
register("aliced")
while True:
    time.sleep(2)
    print '+2'
    reset("aliced")
'''    
