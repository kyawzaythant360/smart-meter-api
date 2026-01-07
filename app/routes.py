from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

from app.database import (
    facilitators_collection,
    usage_collection,
    refresh_tokens_collection
)
from app.auth import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
    oauth2_scheme,
    SECRET_KEY,
    ALGORITHM
)
from app.schemas import (
    FacilitatorRegister,
    UsageCreate,
    TokenPair,
    RefreshTokenRequest
)

router = APIRouter()


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token required"
            )

        return payload["sub"]

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_facilitator(data: FacilitatorRegister):
    existing = await facilitators_collection.find_one({"name": data.name})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Facilitator name already registered"
        )

    await facilitators_collection.insert_one({
        "name": data.name,
        "hashed_password": hash_password(data.password)
    })

    return {"message": "Facilitator registered successfully"}

@router.post("/login", response_model=TokenPair)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await facilitators_collection.find_one({"name": form_data.username})

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(user["name"])
    refresh_token = create_refresh_token(user["name"])

    await refresh_tokens_collection.insert_one({
        "facilitator": user["name"],
        "refresh_token": refresh_token
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenPair)
async def refresh_token(data: RefreshTokenRequest):
    try:
        payload = jwt.decode(
            data.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        stored = await refresh_tokens_collection.find_one({
            "refresh_token": data.refresh_token
        })
        if not stored:
            raise HTTPException(status_code=401, detail="Refresh token revoked")

        subject = payload["sub"]

        new_access = create_access_token(subject)
        new_refresh = create_refresh_token(subject)

        await refresh_tokens_collection.delete_one({
            "refresh_token": data.refresh_token
        })

        await refresh_tokens_collection.insert_one({
            "facilitator": subject,
            "refresh_token": new_refresh
        })

        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.post("/usage")
async def add_usage(
    usage: UsageCreate,
    facilitator: str = Depends(get_current_user)
):
    await usage_collection.insert_one({
        "facilitator_name": facilitator,
        "kilowatts_used": usage.kilowatts_used
    })

    return {"message": "Usage recorded"}


@router.get("/usage")
async def get_my_usage(facilitator: str = Depends(get_current_user)):
    records = []

    async for record in usage_collection.find(
        {"facilitator_name": facilitator}
    ):
        record["_id"] = str(record["_id"])
        records.append(record)

    return records
