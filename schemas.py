from typing import Optional
from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    info: str
    adres: str
    phone_number: str



class CompanyResponse(CompanyCreate):
    id: int

    class Config:
        from_attributes = True


class BuildingCreate(BaseModel):
    name : str
    adres : str
    image: Optional[str] = None
    sertificate: Optional[str] = None
    company_id : int
 
 
class BuildingResponse(BuildingCreate):
    id: int

    class Config:
        from_attributes = True