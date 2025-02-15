from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    userName:Mapped[str]=mapped_column(String(255),unique=True,nullable=False)
    email:Mapped[str] = mapped_column(String(255), unique=True,nullable=False)
    firstName: Mapped[str] = mapped_column(String(255), nullable=True)
    secondName: Mapped[str] = mapped_column(String(255), nullable=True)

