from typing import List

from pydantic import BaseModel

from .address import AddressOut


class UserOut(BaseModel):
    id: int
    username: str
    addresses: List[AddressOut] = []


class UserIn(BaseModel):
    username: str
