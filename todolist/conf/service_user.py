import itertools

from oslo_config import cfg

service_user_group = cfg.OptGroup(
    "service_user",
    title="Service token authentication type options",
    help="""
Configuration options for service to service authentication using a service
token. These options allow to send a service token along with the
user's token when contacting external REST APIs.
""",
)
service_user_opts = [
    cfg.BoolOpt(
        "send_service_user_token",
        default=False,
        help="""
When True, if sending a user token to an REST API, also send a service token.
""",
    ),
    cfg.StrOpt(
        "interface",
        default="internal",
        help="""
Interface to use for the Identity API endpoint. Valid values are "public",
"internal" (default) or "admin".
""",
    ),
]


def register_opts(conf):
    conf.register_group(service_user_group)
    conf.register_opts(service_user_opts, group=service_user_group)


def list_opts():
    return {
        service_user_group: itertools.chain(
            service_user_opts,
        )
    }
