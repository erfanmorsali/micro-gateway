from pydantic import BaseModel


class AddressOut(BaseModel):
    id: int
    country: str
    city: str
    userId: int


class AddressIn(BaseModel):
    country: str
    city: str
    userId: int
