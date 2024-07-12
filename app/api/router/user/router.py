from typing import Optional, List

from fastapi import APIRouter, Depends
from starlette import status

from .schema import CreateUserRequest
from .service import UserService
from dependency import db


router = APIRouter()
@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create account user",
)
async def create_account_user(
        dto: CreateUserRequest,
        service: AccountService = Depends(AccountService),
        vendor_service: VendorService = Depends()
) -> model.Account:
    await vendor_service.get_vendor(dto.vendor_id)
    return await service.create_account(dto)


@router.put(
    "/password/{login_id}",
    summary="Change password",
    dependencies=[Depends(is_yourself_account)],
)
async def change_password(
        login_id: str,
        dto: ChangePasswordRequest,
        service: AccountService = Depends(AccountService),
):
    await service.change_password(login_id, dto)
    return "success change password"


@router.put(
    "/{login_id}",
    summary="Update account info",
    dependencies=[Depends(is_yourself_account)],
)
async def update_specific_account_info(
        login_id: str,
        dto: UpdateAccountRequest,
        service: AccountService = Depends(),
) -> model.Account:
    await service.update_account_info(login_id, dto)
    return await service.get_account_by_id(login_id)
