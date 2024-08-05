from oslo_config import cfg

todolist_group = cfg.OptGroup(
    name="todolist",
    title="TodoList Options",
    help="""
TodoList related options.
""",
)

todolist_opts = [
    cfg.BoolOpt(
        "enable_api_doc",
        default=True,
        help="""
Enable api doc.
""",
    ),
]


def register_opts(conf):
    conf.register_group(todolist_group)
    conf.register_opts(todolist_opts, group=todolist_group)


def list_opts():
    return {todolist_group: todolist_opts}
