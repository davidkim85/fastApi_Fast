from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    userName:str
    email: EmailStr
    firstName: str
    secondName: str

    class Config:
        from_attributes = True

class UserPartialUpdate(BaseModel):
    firstName: str or None = None
    secondName: str or None = None

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

