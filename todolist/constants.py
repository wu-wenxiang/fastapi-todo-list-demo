from enum import Enum

# Base Information
PROJECT_NAME: str = "todolist"
API_V1_STR: str = "/api/v1"
CONFIG_FILE_PATH: str = "/etc/todolist/todolist.conf"

# X-Auth-Token
X_AUTH_TOKEN: str = "X-Auth-Token"


class MessageEnum(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
