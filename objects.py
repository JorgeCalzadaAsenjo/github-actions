from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(description="Id del item", ge=0)
    name: str = Field(description="Nombre del usuario", min_length=3)
    password: str = Field(description="Contraseña del usuario", min_length=3)

class Item(BaseModel):
    id: int = Field(description="Id del item", ge=0)
    name: str = Field(description="Nombre del item", min_length=3)
    price: float = Field(description="Precio", gt=0)
    is_offer: bool = Field(description="Se vende?")


class Db(BaseModel):
    users: list[User]
    items: list[Item]


