from logging import LoggerAdapter
from typing import Optional

from fastapi import Request, Response, status
from oslo_config import cfg
from oslo_log import log as logging
from sqlalchemy import exc as sql_exc

from todolist import exception
from todolist.db import api as db_api, models
from todolist.schemas import todoelems as ds_schema

LOG: LoggerAdapter = logging.getLogger(__name__)
CONF = cfg.CONF


def hello(request: Request, response: Response, hello_id: int):
    return {"message": f"Hello World {hello_id}"}


def list_todoelems(request: Request, response: Response, name: Optional[str] = None):
    todoelems = db_api.todoelem_get_all(name)
    return ds_schema.TodoelemListResponse(
        todoelems=[ds_schema.TodoelemResponseBase(**ds.to_dict()) for ds in todoelems]
    )


def show_todoelems(reqeust: Request, response: Response, todoelem_id: int):
    try:
        todoelem = db_api.todoelem_get(todoelem_id)
    except sql_exc.NoResultFound:
        err_msg = f"Todoelem with id {todoelem_id} not found"
        LOG.exception(err_msg)
        raise exception.TodoelemNotFound(message=err_msg)
    return ds_schema.TodoelemShowResponse(
        todoelem=ds_schema.TodoelemResponseBase(**todoelem.to_dict())
    )


def create_todoelems(request: Request, response: Response, todoelem: ds_schema.TodoelemCreate):
    in_todoelem = models.Todoelem(**todoelem.model_dump())
    todoelem = db_api.todoelem_create(in_todoelem)
    return ds_schema.TodoelemShowResponse(
        todoelem=ds_schema.TodoelemResponseBase(**todoelem.to_dict())
    )


def update_todoelems(
    request: Request, response: Response, todoelem_id: int, todoelem: ds_schema.TodoelemUpdate
):
    in_todoelem = todoelem.model_dump()
    try:
        todoelem = db_api.todoelem_update(todoelem_id, in_todoelem)
    except sql_exc.NoResultFound:
        err_msg = f"Todoelem with id {todoelem_id} not found"
        LOG.exception(err_msg)
        raise exception.TodoelemNotFound(message=err_msg)
    return ds_schema.TodoelemUpdateResponse(
        todoelem=ds_schema.TodoelemUpdateResponseBase(**todoelem.to_dict())
    )


def delete_todoelems(request: Request, response: Response, todoelem_id: int):
    db_api.todoelem_delete(todoelem_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
