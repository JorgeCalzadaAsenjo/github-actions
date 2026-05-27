from pydantic import BaseModel, Field

from schemas.item import Item
from schemas.user import User


class Db(BaseModel):
    users: list[User]
    items: list[Item]


