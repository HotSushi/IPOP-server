from threading import Timer
import urllib
import urllib2

running_timers = {}

def setJidStopped(jid):
    #print jid + 'stopped'
    kill(jid)
    data = urllib.urlencode({'type':'change_status','xmppid':jid,'status':'stopped'})
    urllib2.urlopen('http://127.0.0.1:8000/IPOP/default/set?%s'%(data))
    
#after 5 minutes the function will go off
def beat(jid):
    if jid in running_timers:
        kill(jid)
    running_timers[jid] = Timer(10,setJidStopped, [jid])
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
