from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta, timezone
from bson import ObjectId
from jose import jwt, JWTError
import random

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
    SECRET_KEY,
    ALGORITHM
)

router = APIRouter()


# -------------------------------
# Schemas
# -------------------------------
class FacilitatorRegister(BaseModel):
    name: str
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class SimUsageRequest(BaseModel):
    access_token: str
    product_id: str
    start: datetime | None = None
    end: datetime | None = None
    page: int = 1
    per_page: int = 10


class SimUsageResponse(BaseModel):
    product_id: str
    dateCreated: datetime
    generatedEnergyWh: float
    generatedEnergyTotalWh: float
    soldEnergyWh: float
    boughtEnergyWh: float



def to_utc_naive(dt: datetime) -> datetime:
    """
    Convert timezone-aware datetime to UTC naive (MongoDB compatible)
    """
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt
# -------------------------------
# Auth Helpers
# -------------------------------
def validate_token(token: str) -> str:
    """
    Validate access token and return facilitator name.
    """
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


async def get_current_user(authorization: str = Header(...)):
    """
    Extract token from 'Authorization: Bearer <token>' header and validate.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    token = authorization.split(" ")[1]
    return validate_token(token)


# -------------------------------
# Auth Routes
# -------------------------------
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
        payload = jwt.decode(data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

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


# -------------------------------
# POST Usage Route (token in body)
# -------------------------------
@router.post("/products/sim", response_model=List[SimUsageResponse])
async def get_product_sim_usage_post(req: SimUsageRequest):
    """
    Fetch SIM usage records for a product.
    Requires access token in JSON body.
    Supports optional date range, pagination.
    """
    facilitator = validate_token(req.access_token)

    query = {
        "product_id": ObjectId(req.product_id),
        "facilitator_name": facilitator
    }

    if start:
        start_utc = start.astimezone(timezone.utc).replace(tzinfo=None)
        query["dateCreated"]["$gte"] = start_utc    
    if end:
        end_utc = end.astimezone(timezone.utc).replace(tzinfo=None)
        query["dateCreated"]["$lte"] = end_utc


    skip = (req.page - 1) * req.per_page

    cursor = usage_collection.find(query).sort("dateCreated", -1).skip(skip).limit(req.per_page)
    results = []

    async for record in cursor:
        results.append({
            "product_id": str(record["product_id"]),
            "dateCreated": record["dateCreated"],
            "generatedEnergyWh": record["generatedEnergy_wh"],
            "generatedEnergyTotalWh": record["generatedEnergyTotal_wh"],
            "soldEnergyWh": record["soldEnergy_wh"],
            "boughtEnergyWh": record["boughtEnergy_wh"]
        })

    return results


# -------------------------------
# GET Usage Route (token via header)
# -------------------------------
@router.get("/products/{product_id}/sim", response_model=List[SimUsageResponse])
async def get_product_sim_usage(
    product_id: str,
    start: datetime | None = Query(None),
    end: datetime | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
):
    query = {
        "product_id": ObjectId(product_id),
        "facilitator_name": "demo_facilitator"
    }

    if start or end:
        query["dateCreated"] = {}

        if start:
            query["dateCreated"]["$gte"] = to_utc_naive(start)
        if end:
            query["dateCreated"]["$lte"] = to_utc_naive(end)

    skip = (page - 1) * per_page

    cursor = (
        usage_collection
        .find(query)
        .sort("dateCreated", -1)
        .skip(skip)
        .limit(per_page)
    )

    results = []
    async for record in cursor:
        results.append({
            "product_id": str(record["product_id"]),
            "dateCreated": record["dateCreated"],
            "generatedEnergyWh": record["generatedEnergy_wh"],
            "generatedEnergyTotalWh": record["generatedEnergyTotal_wh"],
            "soldEnergyWh": record["soldEnergy_wh"],
            "boughtEnergyWh": record["boughtEnergy_wh"],
        })

    return results


# -------------------------------
# Demo / Populate Route (No Auth)
# -------------------------------
FIXED_PRODUCT_ID = ObjectId("6964bf4daf5f95aeaff1b7be")  # example

@router.post("/demo/populate")
async def populate_demo_data(
    num_days: int = 30,
    facilitator_name: str = "demo_facilitator"
):
    """
    Populate MongoDB with demo usage data for a fixed product ID.
    No auth required. Each day will have different usage data.
    """
    inserted_count = 0

    product_id = FIXED_PRODUCT_ID
    total_generated = 0

    for day_offset in range(num_days):
        date_created = datetime.utcnow() - timedelta(days=(num_days - day_offset))
        generated = random.randint(800, 1500)  # Wh
        total_generated += generated
        sold = random.randint(100, min(500, generated))
        bought = random.randint(50, 300)

        document = {
            "product_id": product_id,
            "facilitator_name": facilitator_name,
            "dateCreated": date_created,
            "generatedEnergy_wh": generated,
            "generatedEnergyTotal_wh": total_generated,
            "soldEnergy_wh": sold,
            "boughtEnergy_wh": bought
        }

        await usage_collection.insert_one(document)
        inserted_count += 1

    return {
        "message": f"Demo data populated for product {product_id}, {num_days} days of data.",
        "records_inserted": inserted_count,
        "product_id": str(product_id)
    }