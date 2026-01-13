from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# -------------------------------
# Facilitator Schemas
# -------------------------------
class FacilitatorRegister(BaseModel):
    # Matches the field in your DB
    name: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class FacilitatorCreate(BaseModel):
    # Optional, for internal creation
    name: str
    password: str


class Facilitator(BaseModel):
    # How it is stored in DB
    id: Optional[str]
    name: str
    hashed_password: str


# -------------------------------
# Auth / Token Schemas
# -------------------------------
class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# -------------------------------
# Usage Schemas
# -------------------------------
class UsageCreate(BaseModel):
    # For POST creation of usage
    generatedEnergyWh: float
    generatedEnergyTotalWh: float
    soldEnergyWh: float
    boughtEnergyWh: float
    dateCreated: Optional[datetime] = None


class SimUsageResponse(BaseModel):
    product_id: str
    dateCreated: datetime
    generatedEnergyWh: float
    generatedEnergyTotalWh: float
    soldEnergyWh: float
    boughtEnergyWh: float
