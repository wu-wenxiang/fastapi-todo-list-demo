from logging import LoggerAdapter
from typing import Optional

from fastapi import APIRouter, Body, Header, Path, Query, Request, Response, status
from oslo_config import cfg
from oslo_log import log

from todolist import constants
from todolist.api import manager as api_manager
from todolist.schemas import todoelems as ds_schema

CONF = cfg.CONF
LOG: LoggerAdapter = log.getLogger(__name__)

router = APIRouter()


@router.post(
    "",
    response_model=ds_schema.TodoelemCreateResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create a new todoelem.",
    responses={
        status.HTTP_201_CREATED: {
            "model": ds_schema.TodoelemCreateResponse,
            "description": "Created",
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    },
)
def todoelem_create(
    request: Request,
    response: Response,
    _: str = Header(..., alias=constants.X_AUTH_TOKEN),
    todoelem: ds_schema.TodoelemCreate = Body(
        ...,
        description="Todoelem to create",
        alias="todoelem",
        embed=True,
    ),
):
    LOG.info(f"Create a todoelem: {todoelem}")
    return api_manager.create_todoelems(request, response, todoelem)


@router.get(
    "",
    response_model=ds_schema.TodoelemListResponse,
    status_code=status.HTTP_200_OK,
    description="List todoelems.",
    responses={
        status.HTTP_200_OK: {
            "model": ds_schema.TodoelemListResponse,
            "description": "OK",
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    },
)
def todoelems_list(
    request: Request,
    response: Response,
    _: str = Header(..., alias=constants.X_AUTH_TOKEN),
    name: Optional[str] = Query(None, description="Name of the todoelem"),
):
    LOG.info(f"List todoelems, name: {name}")
    return api_manager.list_todoelems(request, response, name)


@router.get(
    "/{todoelem_id}",
    response_model=ds_schema.TodoelemShowResponse,
    status_code=status.HTTP_200_OK,
    description="Show todoelem.",
    responses={
        status.HTTP_200_OK: {
            "model": ds_schema.TodoelemShowResponse,
            "description": "OK",
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    },
)
def todoelem_show(
    request: Request,
    response: Response,
    _: str = Header(..., alias=constants.X_AUTH_TOKEN),
    todoelem_id: int = Path(..., description="ID of the todoelem"),
):
    LOG.info(f"Show todoelem, todoelem_id: {todoelem_id}")
    return api_manager.show_todoelems(request, response, todoelem_id)


@router.put(
    "/{todoelem_id}",
    response_model=ds_schema.TodoelemUpdateResponse,
    status_code=status.HTTP_200_OK,
    description="Update operation node.",
    responses={
        status.HTTP_200_OK: {
            "model": ds_schema.TodoelemUpdateResponse,
            "description": "OK",
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    },
)
def todoelem_update(
    request: Request,
    response: Response,
    _: str = Header(..., alias=constants.X_AUTH_TOKEN),
    todoelem_id: int = Path(..., description="ID of the todoelem"),
    todoelem: ds_schema.TodoelemUpdate = Body(
        ...,
        description="Todoelem to update",
        alias="todoelem",
        embed=True,
    ),
):
    LOG.info(f"Update a todoelem, todoelem_id: {todoelem_id}, todoelem: {todoelem}")
    return api_manager.update_todoelems(request, response, todoelem_id, todoelem)


@router.delete(
    "/{todoelem_id}",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a todoelem.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    },
)
def todoelem_delete(
    request: Request,
    response: Response,
    _: str = Header(..., alias=constants.X_AUTH_TOKEN),
    todoelem_id: int = Path(..., description="ID of the todoelem"),
):
    LOG.info(f"Delete a todoelem, todoelem_id: {todoelem_id}")
    return api_manager.delete_todoelems(request, response, todoelem_id)
