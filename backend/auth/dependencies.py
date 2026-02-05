from fastapi import Depends, HTTPException, status, Header
from typing import Dict
from .jwt_utils import decode_and_validate_jwt


async def get_current_user(authorization: str = Header(None)) -> str:
    """
    Authentication dependency that extracts and validates JWT token
    Returns the user_id from the token payload
    Raises 401 if token is missing, invalid, or expired
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required"
        )

    # Check if the header follows the Bearer format
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must start with 'Bearer '"
        )

    # Extract the token from the header
    token = authorization.split(" ")[1]

    # Decode and validate the JWT token
    payload = decode_and_validate_jwt(token)

    # Extract user_id from the payload (checking both "user_id" and "sub" claims)
    user_id = payload.get("user_id") or payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not contain valid user identifier"
        )

    return user_id