from oslo_config import cfg
from oslo_context import context
from oslo_log import log as logging

CONF = cfg.CONF

LOG = logging.getLogger(__name__)

RequestContext = context.RequestContext
