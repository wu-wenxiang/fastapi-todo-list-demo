from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from todolist.constants import MessageEnum


class TodoelemCreate(BaseModel):
    name: Optional[str] = Field(None, description="")
    description: Optional[str] = Field(None, description="")


class TodoelemCreateResponseBase(TodoelemCreate):
    id: int = Field(..., description="")
    created_at: Optional[datetime] = Field(None, description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Update time")


class TodoelemResponseBase(BaseModel):
    id: int = Field(..., description="")
    name: Optional[str] = Field(None, description="")
    description: Optional[str] = Field(None, description="")
    created_at: Optional[datetime] = Field(None, description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Update time")


class TodoelemCreateResponse(BaseModel):
    todoelem: TodoelemCreateResponseBase = Field(..., description="Todoelem")


class TodoelemListResponse(BaseModel):
    todoelems: List[TodoelemResponseBase] = Field(..., description="List of todoelems")


class TodoelemShowResponse(BaseModel):
    todoelem: TodoelemResponseBase = Field(..., description="Todoelem")


class TodoelemUpdateResponseBase(TodoelemCreateResponseBase):
    """"""


class TodoelemUpdate(TodoelemCreate):
    """"""


class TodoelemUpdateResponse(BaseModel):
    todoelem: TodoelemUpdateResponseBase = Field(..., description="Todoelem")


class TodoelemUploadCSVResponse(BaseModel):
    message: MessageEnum = Field(
        MessageEnum.SUCCESS, description="Message of the todoelem upload csv response."
    )
