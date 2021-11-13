from typing import List

from circuitbreaker import CircuitBreakerError
from fastapi import APIRouter, HTTPException
from requests.exceptions import RequestException
from starlette.requests import Request

from limiter import limiter
from schemas.address import AddressIn, AddressOut
from services.addresses.address_remote_service import AddressRemoteService

router = APIRouter()
address_remote_service = AddressRemoteService()


@router.get("/addresses", response_model=List[AddressOut])
@limiter.limit("60/minute")
def get_all_addresses(request: Request):
    try:
        # get all addresses
        address_response, address_status = address_remote_service.fetch_all_address()
        if address_status != 200:
            raise HTTPException(address_status, address_response)

    # if RequestException raised
    except RequestException as e:
        raise HTTPException(500, "internal")

    # if CircuitBreakerError raised
    except CircuitBreakerError as e:
        raise HTTPException(500, "wait for 2 minutes")

    return address_response


@router.get("/addresses/{user_id}/", response_model=List[AddressOut])
@limiter.limit("60/minute")
def get_user_addresses(user_id: int, request: Request):
    try:
        # get user addresses
        address_response, address_status = address_remote_service.fetch_user_addresses(user_id)
        if address_status != 200:
            raise HTTPException(address_status, address_response)

    # if RequestException raised
    except RequestException as e:
        raise HTTPException(500, "internal")

    # if CircuitBreakerError raised
    except CircuitBreakerError as e:
        raise HTTPException(500, "wait for 2 minutes")

    return address_response


@router.post("/addresses/create", response_model=AddressOut, status_code=201)
@limiter.limit("60/minute")
def create_address(address_input: AddressIn, request: Request):
    try:
        address_response, address_status = address_remote_service.create_address(address_input)
        if address_status != 201:
            raise HTTPException(address_status, address_response)

    # if RequestException raised
    except RequestException as e:
        raise HTTPException(500, "internal")

    # if CircuitBreakerError raised
    except CircuitBreakerError as e:
        raise HTTPException(500, "wait for 2 minutes")

    return address_response


@router.delete("/addresses/delete/{address_id}/", status_code=204)
@limiter.limit("60/minute")
def delete_address(address_id: int, request: Request):
    try:
        resp = address_remote_service.delete_address(address_id)
        if resp.status_code != 204:
            raise HTTPException(resp.status_code, resp.json())

    # if RequestException raised
    except RequestException as e:
        raise HTTPException(500, "internal")

    # if CircuitBreakerError raised
    except CircuitBreakerError as e:
        raise HTTPException(500, "wait for 2 minutes")

    return ""
