from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(description="Id del item", ge=0)
    name: str = Field(description="Nombre del usuario", min_length=3)
    password: str = Field(description="Contraseña del usuario", min_length=3)
