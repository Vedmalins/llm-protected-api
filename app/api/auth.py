from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User

from jose import JWTError, jwt
from app.config import settings

from app.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)

from app.schemas.user import (
    RefreshTokenSchema,
    TokenResponseSchema,
    UserLoginSchema,
    UserRegisterSchema,
    UserResponseSchema,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegisterSchema, db: AsyncSession = Depends(get_db)):
    existing_user = await db.scalar(
        select(User).where(
            (User.username == user_data.username) | (User.email == user_data.email)
        )
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        is_active=True,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

@router.post("/login", response_model=TokenResponseSchema)
async def login_user(user_data: UserLoginSchema, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(
        select(User).where(User.username == user_data.username)
    )

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token({"sub": str(user.id), "username": user.username})
    refresh_token = create_refresh_token({"sub": str(user.id), "username": user.username})

    return TokenResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=TokenResponseSchema)
async def refresh_access_token(data: RefreshTokenSchema):
    try:
        payload = jwt.decode(
            data.refresh_token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        user_id = payload.get("sub")
        username = payload.get("username")
        token_type = payload.get("type")

        if not user_id or not username or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token",
        )

    access_token = create_access_token({"sub": str(user_id), "username": username})
    refresh_token = create_refresh_token({"sub": str(user_id), "username": username})

    return TokenResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )