from pydantic import BaseModel, EmailStr, Field


class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    model_config = {
        "from_attributes": True
    }

class UserLoginSchema(BaseModel):
    username: str
    password: str


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenSchema(BaseModel):
    refresh_token: str

