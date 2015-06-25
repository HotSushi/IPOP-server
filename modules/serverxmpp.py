from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout


class ServerXmppBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.msgcallback = {}

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

    def get_client_pk(self, client):
            self.send_message(mto = client, mbody = 'get_key ')

def init():
    global instance
    instance = ServerXmppBot('alice_sushant@xmpp.jp', 'alice123')
    instance.connect()
    instance.process(block=False)

'''
if __name__ == '__main__':
    xmpp = ServerBot('alice_sushant@xmpp.jp', 'alice123')
    xmpp.connect()
    xmpp.process(block=False)
    xmpp.get_client_pk('bob_sushant@xmpp.jp')
'''
