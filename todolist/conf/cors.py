from oslo_config import cfg

cors_group = cfg.OptGroup(
    name="cors",
    title="CORS Options",
    help="""
CORS related options.
""",
)

cors_opts = [
    cfg.ListOpt(
        "origins",
        default=[],
        help="""
CORS origins.
""",
    ),
]


def register_opts(conf):
    conf.register_group(cors_group)
    conf.register_opts(cors_opts, group=cors_group)


def list_opts():
    return {cors_group: cors_opts}
