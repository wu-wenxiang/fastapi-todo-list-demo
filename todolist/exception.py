import six
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class TodoListException(Exception):

    message = "An unknown exception occurred."
    code = 500
    headers: dict = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs
        self.kwargs["message"] = message

        if "code" not in self.kwargs:
            try:
                self.kwargs["code"] = self.code
            except AttributeError:
                pass

        for k, v in self.kwargs.items():
            if isinstance(v, Exception):
                self.kwargs[k] = six.text_type(v)

        if self._should_format():
            try:
                message = self.message % kwargs

            except Exception:
                self._log_exception()
                message = self.message
        elif isinstance(message, Exception):
            message = six.text_type(message)

        self.msg = message
        super(TodoListException, self).__init__(message)
        self.kwargs.pop("message", None)

    def _log_exception(self):
        LOG.exception("Exception in string format operation:")
        for name, value in self.kwargs.items():
            LOG.error("%(name)s: %(value)s", {"name": name, "value": value})

    def _should_format(self):
        return self.kwargs["message"] is None or "%(message)" in self.message

    def __unicode__(self):
        return self.msg


class NotAuthorized(TodoListException):
    message = "Not authorized."
    code = 403


class NotFound(TodoListException):
    message = "An object with the specified identifier was not found."
    code = 404


class TodoelemNotFound(NotFound):
    message = "Todoelem %(todoelem_id)s not found."


class BadRequest(TodoListException):
    message = (
        "The server could not comply with the request since it is either "
        "malformed or otherwise incorrect."
    )
    code = 400


class TodoelemUploadCSVInvalidFileType(BadRequest):
    message = "Invalid file type. Please upload a CSV file."
