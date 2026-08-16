from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class JuradoCreate(BaseModel):
    nombre: str = Field(
        min_length=1,
        max_length=200
    )

    email: EmailStr

    cognito_sub: str | None = None


class JuradoUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    email: EmailStr | None = None

    cognito_sub: str | None = None

    activo: bool | None = None


class JuradoResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    cognito_sub: str | None
    nombre: str
    email: EmailStr
    activo: bool
    created_at: datetime
    updated_at: datetime