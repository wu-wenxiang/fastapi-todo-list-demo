import collections
import importlib
import os
import pkgutil

LIST_OPTS_FUNC_NAME = "list_opts"


def _tupleize(dct):
    """Take the dict of options and convert to the 2-tuple format."""
    return [(key, val) for key, val in dct.items()]


def list_opts():
    opts: collections.defaultdict = collections.defaultdict(list)
    module_names = _list_module_names()
    imported_modules = _import_modules(module_names)
    _append_config_options(imported_modules, opts)
    return _tupleize(opts)


def _list_module_names():
    module_names = []
    package_path = os.path.dirname(os.path.abspath(__file__))
    for _, modname, ispkg in pkgutil.iter_modules(path=[package_path]):
        if modname == "opts" or ispkg:
            continue
        else:
            module_names.append(modname)
    return module_names


def _import_modules(module_names):
    imported_modules = []
    for modname in module_names:
        mod = importlib.import_module("todolist.conf." + modname)
        if not hasattr(mod, LIST_OPTS_FUNC_NAME):
            msg = (
                "The module 'todolist.conf.%s' should have a '%s' "
                "function which returns the config options." % (modname, LIST_OPTS_FUNC_NAME)
            )
            raise Exception(msg)
        else:
            imported_modules.append(mod)
    return imported_modules


def _append_config_options(imported_modules, config_options):
    for mod in imported_modules:
        configs = mod.list_opts()
        for key, val in configs.items():
            config_options[key].extend(val)
