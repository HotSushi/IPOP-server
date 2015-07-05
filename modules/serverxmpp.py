from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout


class ServerXmppBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.jid = jid
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.msgcallback = {}

    def change_instance(self,admin_jid,admin_password):
        if self.jid == admin_jid:
            return
        self.__init__( admin_jid,admin_password)
        connect()
        process(block = False)

    def add_callback(self, function_name, function_addr):
        self.msgcallback[function_name] = function_addr

    def session_start(self, event):
        self.send_presence()
        self.get_roster()


    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msgs = msg['body'].split(' ',2)

            if msgs[0] == 'register':
                client_jid = msgs[1]
                pk = msgs[2]
                msg.reply('received_key_ack ').send()
                #callback on 'on_key_recvd'
                if 'on_key_recvd' in self.msgcallback.keys():
                    self.msgcallback['on_key_recvd'](client_jid, pk)
            else:
                #add other messages here
                pass

    def get_admin_jid(self):
        return self.jid            

    def get_client_pk(self, client):
        self.send_message(mto = client, mbody = 'get_key ')

    def send_key_ack(self, client):
        self.send_message(mto = client, mbody = 'received_key_ack ')

    def stop_client(self, client):
        self.send_message(mto = client, mbody = 'stop_node ')

    def change_ip(self, client):
        self.send_message(mto = client, mbody = 'change_ip ')

    
def init():
    global instance
    instance = ServerXmppBot('alice_sushant@xmpp.jp', 'alice123')
    instance.connect()
    instance.process(block=False)

def change_instance(admin_jid,admin_password):
    global instance
    if instance.get_admin_jid() == admin_jid:
        return

    print 'changed admin to '+ admin_jid
    instance = ServerXmppBot(admin_jid , admin_password)
    instance.connect()
    instance.process(block = False)


'''
if __name__ == '__main__':
    xmpp = ServerBot('alice_sushant@xmpp.jp', 'alice123')
    xmpp.connect()
    xmpp.process(block=False)
    xmpp.get_client_pk('bob_sushant@xmpp.jp')
'''
