from typing import List

from fastapi import APIRouter, HTTPException

from schemas.address import AddressIn, AddressOut
from services.addresses.address_remote_service import AddressRemoteService

router = APIRouter()
address_remote_service = AddressRemoteService()


@router.get("/addresses", response_model=List[AddressOut])
def get_all_addresses():
    address_response, address_status = address_remote_service.fetch_all_address()
    if address_status != 200:
        raise HTTPException(address_status, address_response)

    return address_response


@router.get("/addresses/{user_id}/", response_model=List[AddressOut])
def get_user_addresses(user_id: int):
    address_response, address_status = address_remote_service.fetch_user_addresses(user_id)
    if address_status != 200:
        raise HTTPException(address_status, address_response)

    return address_response


@router.post("/addresses/create", response_model=AddressOut, status_code=201)
def create_address(address_input: AddressIn):
    address_response, address_status = address_remote_service.create_address(address_input)
    if address_status != 201:
        raise HTTPException(address_status, address_response)

    return address_response


@router.delete("/addresses/delete/{address_id}/", status_code=204)
def delete_address(address_id: int):
    resp = address_remote_service.delete_address(address_id)
    if resp.status_code != 204:
        raise HTTPException(resp.status_code, resp.json())

    return ""
