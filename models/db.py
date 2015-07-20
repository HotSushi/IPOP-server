db = DAL("sqlite://storage.sqlite")

db.define_table('vpn',
                db.Field('vpn_name', 'string', required=False, length=255),
                db.Field('description', 'text', required=False, default=''),
                db.Field('admin_jid', 'string', required=False ),
                db.Field('admin_password', 'string', required=False ),
                db.Field('ipv4_mask', 'integer', required=False),
                db.Field('ejabberd_password','string', required=False, default='')
                )

db.define_table('xmpnode',
                db.Field('jid', 'string', required=False, length=255),
                db.Field('password', 'string', required=False),
                db.Field('ip', 'string', required=False),
                db.Field('xmpp_host', 'string', required=False),
                db.Field('vpn_id',  db.vpn),
                db.Field('status', 'string', default=''),
                db.Field('public_key','text')
                )

db.define_table('logs',
                db.Field('node','string'),
                db.Field('name','string'),
                db.Field('log','text', default='')
                )

db.define_table('users',
                db.Field('username','string',required=True),
                db.Field('password','string',required=True)
                )

#add default username password
if len(db(db.users).select()) == 0:
    db.users.insert(username='user',password='password')
