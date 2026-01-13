from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Facilitator(BaseModel):
    id: Optional[str]
    name: str
    hashed_password: str

class SimUsageCreate(BaseModel):
    product_id: str
    generatedEnergyWh: float
    soldEnergyWh: float
    boughtEnergyWh: float
    
class SimUsageResponse(BaseModel):
    product_id: str
    dateCreated: datetime
    generatedEnergyWh: float
    generatedEnergyTotalWh: float
    soldEnergyWh: float
    boughtEnergyWh: float