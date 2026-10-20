
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str


class Prediction(SQLModel, table=True):
    __tablename__ = "predictions"

    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="users.id")
    ticket_text: str
    predicted_category: str
