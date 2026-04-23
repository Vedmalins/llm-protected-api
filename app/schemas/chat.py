from pydantic import BaseModel, Field


class ChatRequestSchema(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)


class ChatResponseSchema(BaseModel):
    user_message: str
    assistant_message: str

class ChatMessageSchema(BaseModel):
    id: int
    role: str
    content: str

    model_config = {
        "from_attributes": True
    }