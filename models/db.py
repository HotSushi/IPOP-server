db = DAL("sqlite://storage.sqlite")

db.define_table('vpn',
                db.Field('vpn_name', 'string', required=False, length=255),
                db.Field('description', 'text', required=False, default=''),
                db.Field('ipv4_mask', 'integer', required=False)
                )

db.define_table('xmpnode',
                db.Field('jid', 'string', required=False, length=255),
                db.Field('password', 'string', required=False),
                db.Field('ip', 'string', required=False),
                db.Field('xmpp_host', 'string', required=False),
                db.Field('vpn_name', 'string', required=False),
                db.Field('public_key','text')
                )

db.vpn.vpn_name.requires = IS_NOT_IN_DB(db, db.vpn.vpn_name)
db.xmpnode.vpn_name.requires = IS_IN_DB(db, db.vpn.vpn_name)
