from oslo_config import cfg

database_group = cfg.OptGroup(
    name="database",
    title="Database Options",
    help="""
Database related options.
""",
)

database_opts = [
    cfg.StrOpt(
        "connection",
        default="sqlite:///todolist.db",
        # default="mysql+pymysql://root:root@127.0.0.1:3306/todolist",
        help="""
Database connection.
""",
    ),
    cfg.IntOpt(
        "max_pool_size",
        default=50,
        help="""
Maximum number of SQL connections to keep open in a pool.
Setting a value of 0 indicates no limit.
""",
    ),
    cfg.IntOpt(
        "max_overflow",
        default=1000,
        help="""
If set, use this value for max_overflow with sqlalchemy.
""",
    ),
]


def register_opts(conf):
    conf.register_group(database_group)
    conf.register_opts(database_opts, group=database_group)


def list_opts():
    return {database_group: database_opts}
