# app/schemas/post.py
import datetime
from pydantic import BaseModel, Field, validator

class PostCreate(BaseModel):
    """
    Pydantic model for creating a new post.
    """
    text: str = Field(...)

    @validator("text")
    def validate_text_size(cls, v):
        # Validate that the text size does not exceed 1 MB
        if len(v.encode("utf-8")) > 1024 * 1024:
            raise ValueError("Payload exceeds 1 MB")
        return v

class PostOut(BaseModel):
    """
    Pydantic model for outputting post data.
    """
    id: int
    text: str
    created_at: datetime.datetime

    class Config:
        # Enable loading data from ORM objects using attributes
        from_attributes = True
