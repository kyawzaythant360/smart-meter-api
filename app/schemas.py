from pydantic import BaseModel, Field

class FacilitatorCreate(BaseModel):
    company_id: str
    password: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UsageCreate(BaseModel):
    kilowatts_used: float

class FacilitatorRegister(BaseModel):
    company_id: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
