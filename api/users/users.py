from fastapi import Query, Depends, HTTPException, status, APIRouter
from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from configurations.database import get_async_session
from models.userModel import User
from schemas.userSchema import UserRead, UserPartialUpdate, UserCreate

usersRouter = APIRouter()

async def pagination(skip: int = Query(0, ge=0),limit: int = Query(10, ge=0),) -> tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


async def get_user_or_404(id: int, session: AsyncSession = Depends(get_async_session)) -> User:
    select_query = (select(User).where(User.id == id))
    result = await session.execute(select_query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@usersRouter.get("/", response_model=list[UserRead])
async def list_users(pagination: tuple[int, int] = Depends(pagination),session: AsyncSession = Depends(get_async_session)) -> Sequence[User]:
    skip, limit = pagination
    select_query = (select(User).offset(skip).limit(limit))
    result = await session.execute(select_query)
    return result.scalars().all()


@usersRouter.get("/{id}", response_model=UserRead)
async def get_user(user: User = Depends(get_user_or_404)) -> User:
    return user


@usersRouter.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_create:UserCreate, session: AsyncSession = Depends(get_async_session)) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    return user


@usersRouter.patch("/{id}", response_model=UserRead)
async def update_user(user_update:UserPartialUpdate,user: User = Depends(get_user_or_404),
    session: AsyncSession = Depends(get_async_session)) -> User:
    user_update_dict = user_update.model_dump(exclude_unset=True)
    for key, value in user_update_dict.items():
        setattr(user, key, value)
    session.add(user)
    await session.commit()
    return user


@usersRouter.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: User = Depends(get_user_or_404),session: AsyncSession = Depends(get_async_session)):
    await session.delete(user)
    await session.commit()
