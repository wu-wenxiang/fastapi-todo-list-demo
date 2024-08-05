from fastapi import APIRouter, Header, Path, Request, Response
from oslo_config import cfg

from todolist import constants
from todolist.api import manager as api_manager

CONF = cfg.CONF
router = APIRouter()


@router.get("/{hello_id}")
async def root(
    request: Request,
    response: Response,
    _: str = Header(..., alias=constants.X_AUTH_TOKEN),
    hello_id: int = Path(...),
):
    return api_manager.hello(request, response, hello_id)
