from typing import List

from circuitbreaker import CircuitBreakerError
from fastapi import APIRouter, HTTPException
from requests.exceptions import RequestException
from starlette.requests import Request

from limiter import limiter
from schemas.user import UserIn, UserOut
from services.addresses.address_remote_service import AddressRemoteService
from services.users.user_remote_service import UserRemoteService

router = APIRouter()
user_remote_service = UserRemoteService()
address_remote_service = AddressRemoteService()


@router.get("/users/", response_model=List[UserOut])
@limiter.limit("30/minute")
def get_all_users(request: Request):
    try:
        # get all users
        user_response, user_status = user_remote_service.fetch_all_users()
        if user_status != 200:
            raise HTTPException(user_status, user_response)

    # if RequestException raised :
    except RequestException as e:
        raise HTTPException(500, "Internal")

    # if CircuitBreakerError raised :
    except CircuitBreakerError as e:
        raise HTTPException(500, "wait for 2 minutes")

    try:
        # get all addresses
        address_response, address_status = address_remote_service.fetch_all_address()

        # return only users if address service cant fetch addresses
        if address_status != 200:
            return user_response

    # Return only users if address service is not available
    except Exception:
        return user_response

    # if users and addresses are ready then combine results
    for user in user_response:
        user['addresses'] = []
        for address in address_response:
            user_id = address['userId']
            if user_id == user['id']:
                user['addresses'].append(address)

    return user_response


@router.get("/users/{user_id}", response_model=UserOut)
@limiter.limit("60/minute")
def get_user_by_id(user_id: int, request: Request):
    try:
        # get user
        user_response, user_status = user_remote_service.fetch_single_user(user_id)
        if user_status != 200:
            raise HTTPException(user_status, user_response)

    # if RequestException raised:
    except RequestException as e:
        raise HTTPException(500, "Internal")

    # if CircuitBreakerError raised:
    except CircuitBreakerError as e:
        raise HTTPException(500, "wait for 2 minutes")

    try:
        # get user addresses
        address_response, address_status = address_remote_service.fetch_user_addresses(user_id)

        # if address service cant fetch addresses, just return user
        if address_status != 200:
            return user_response

    except Exception:
        return user_response

    # Combine results if both are ready
    user_response['addresses'] = address_response
    return user_response


@router.post("/users/create", response_model=UserOut, status_code=201)
@limiter.limit("60/minute")
def create_user(user_input: UserIn, request: Request):
    try:
        user_response, user_status = user_remote_service.create_user(user_input)
        if user_status != 201:
            raise HTTPException(user_status, user_response)

    # if RequestException raised
    except RequestException as e:
        raise HTTPException(500, "internal")

    # if CircuitBreakerError raised
    except CircuitBreakerError as e:
        raise HTTPException(500, "wait for 2 minutes")

    return user_response


@router.delete("/users/delete/{user_id}/", status_code=204)
@limiter.limit("40/minute")
def delete_user(user_id: int, request: Request):
    try:
        resp = user_remote_service.delete_user(user_id)
        if resp.status_code != 204:
            raise HTTPException(resp.status_code, resp.json())

    # if RequestException raised
    except RequestException as e:
        raise HTTPException(500, "internal")

    # if CircuitBreakerError raised
    except CircuitBreakerError as e:
        raise HTTPException(500, "wait for 2 minutes")

    return ""
