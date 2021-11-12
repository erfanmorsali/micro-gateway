from typing import List

from fastapi import APIRouter, HTTPException

from schemas.user import UserIn, UserOut
from services.addresses.address_remote_service import AddressRemoteService
from services.users.user_remote_service import UserRemoteService

router = APIRouter()
user_remote_service = UserRemoteService()
address_remote_service = AddressRemoteService()


@router.get("/users/", response_model=List[UserOut])
def get_all_users():
    user_response, user_status = user_remote_service.fetch_all_users()

    if user_status != 200:
        raise HTTPException(user_status, user_response)

    address_response, address_status = address_remote_service.fetch_all_address()
    if address_status != 200:
        raise HTTPException(address_status, address_response)

    for user in user_response:
        user['addresses'] = []
        for address in address_response:
            user_id = address['userId']
            if user_id == user['id']:
                user['addresses'].append(address)

    return user_response


@router.get("/users/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int):
    user_response, user_status = user_remote_service.fetch_single_user(user_id)
    if user_status != 200:
        raise HTTPException(user_status, user_response)

    address_response, address_status = address_remote_service.fetch_user_addresses(user_id)
    if address_status != 200:
        raise HTTPException(address_status, address_response)

    user_response['addresses'] = address_response
    return user_response


@router.post("/users/create", response_model=UserOut, status_code=201)
def create_user(user_input: UserIn):
    user_response, user_status = user_remote_service.create_user(user_input)
    if user_status != 201:
        raise HTTPException(user_status, user_response)

    return user_response


@router.delete("/users/delete/{user_id}/", status_code=204)
def delete_user(user_id: int):
    resp = user_remote_service.delete_user(user_id)
    if resp.status_code != 204:
        raise HTTPException(resp.status_code, resp.json())

    return ""
