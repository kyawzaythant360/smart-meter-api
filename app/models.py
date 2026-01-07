from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Facilitator(BaseModel):
    id: Optional[str]
    name: str
    hashed_password: str

class GeneratorUsage(BaseModel):
    facilitator_name: str
    kilowatts_used: float
    date: datetime = Field(default_factory=datetime.utcnow)
