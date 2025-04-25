from pydantic import BaseModel, Field
from typing import Optional

class PokeRequest(BaseModel):
    id: Optional[int] = Field(
        default=None,
        ge=1,
        description="ID de la petición"
    )

    pokemon_type: Optional[str] = Field(
        default=None,
        description="Tipo de Pokémon",
        pattern="^[a-zA-Z0-9_]+$"
    )

    url : Optional[str] = Field(
        default=None,
        description="URL de la petición",
        pattern="^https?://[a-zA-Z0-9_.-]+(:[0-9]+)?(/.*)?$"
    )

    status: Optional[str] = Field(
        default=None,
        description="Estado de la petición",
        pattern="^(sent|completed|inprogress|failed)$"
    )

    pokemon_qty: Optional[int] = Field(
        default=1,
        ge=1,
        description="Cantidad de Pokémon"     
    )