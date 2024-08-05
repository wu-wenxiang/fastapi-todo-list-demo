from oslo_config import cfg

from . import base, cors, database, service_user, todolist

CONF = cfg.CONF

base.register_opts(CONF)
cors.register_opts(CONF)
todolist.register_opts(CONF)
service_user.register_opts(CONF)
database.register_opts(CONF)
