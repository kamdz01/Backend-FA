# app/schemas/post.py
import datetime
from pydantic import BaseModel, Field, validator

class PostCreate(BaseModel):
    text: str = Field(...)

    @validator("text")
    def validate_text_size(cls, v):
        if len(v.encode("utf-8")) > 1024 * 1024:
            raise ValueError("Payload przekracza 1 MB")
        return v

class PostOut(BaseModel):
    id: int
    text: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True
