import os
import time
import uuid
from contextlib import asynccontextmanager
from logging import LoggerAdapter

from fastapi import FastAPI, Request, applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from oslo_config import cfg
from oslo_log import log as logging
from starlette.middleware.cors import CORSMiddleware

from todolist import conf, constants, db, version
from todolist.api.v1 import api_router

PROJECT_NAME = "TodoList API"
API_PREFIX = "/api/v1"

CONF: cfg = conf.CONF
LOG: LoggerAdapter = logging.getLogger(__name__)


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
        swagger_favicon_url="/static/swagger-ui/favicon-32x32.png",
    )


applications.get_swagger_ui_html = swagger_monkey_patch


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.register_options(CONF)
    config_file = os.environ.get("TODOLIST_CONFIG_DIR", constants.CONFIG_FILE_PATH)
    CONF(
        args=["--config-file", config_file],
        project=constants.PROJECT_NAME,
        version=version.version_string(),
    )
    logging.setup(CONF, constants.PROJECT_NAME)
    if CONF.cors.origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=CONF.cors.origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    db.setup_db()

    if not CONF.todolist.enable_api_doc:
        app.openapi_url = None

    LOG.info(f"Starting {constants.PROJECT_NAME} API")
    yield


app = FastAPI(
    title=constants.PROJECT_NAME,
    openapi_url=f"{constants.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


# Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def add_request_id_header(request: Request, call_next):
    request_id = uuid.uuid4().hex
    LOG.debug(f"Request path: {request.url.path}, request id: {request_id}")
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["TodoList-Request-ID"] = request_id
    return response


app.include_router(api_router, prefix=API_PREFIX)
app.mount(
    "/static",
    StaticFiles(directory=f"{os.path.abspath(os.path.dirname(__file__))}/static"),
    name="static",
)
