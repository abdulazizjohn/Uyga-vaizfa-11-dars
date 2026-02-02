import shutil
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, UploadFile
from models import *
from schemas import * 
from database import MEDIA_DIR


async def reads_company(db : AsyncSession) -> list[CompanyResponse]:
    result = await db.execute(select(Company))
    companies = result.scalars().all()
    return [CompanyResponse.model_validate(company) for company in companies]


async def read_company(company_id : int , db: AsyncSession) -> CompanyResponse:
    db_company = await db.get(Company, company_id)
    if db_company is None:
        raise HTTPException(status_code=404 , detail="Company not found")
    return CompanyResponse.model_validate(db_company)


async def create_company(company : CompanyCreate , db : AsyncSession) -> CompanyResponse:
    db_company = Company(**company.model_dump())
    db.add(db_company)
    await db.commit()
    await db.refresh(db_company)
    return CompanyResponse.model_validate(db_company)




async def update_company(company_id : int , company : CompanyCreate , db : AsyncSession) -> CompanyResponse:
    db_company = await db.get(Company, company_id)
    if db_company is None:
        raise HTTPException(status_code=404 , detail="Company not found")
    for key, value in company:
        setattr(db_company, key, value)
    db.add(db_company)
    await db.commit()
    await db.refresh(db_company)
    return CompanyResponse.model_validate(db_company)



async def delete_company(company_id : int , db : AsyncSession) -> dict:
    db_company = await db.get(Company, company_id)
    if db_company is None:
        raise HTTPException(status_code=404 , detail="Company not found")
    await db.delete(db_company)
    await db.commit()
    return None




async def create_building(building : BuildingCreate , db : AsyncSession, image: UploadFile = None, sertificate: UploadFile = None) -> BuildingResponse:
    if image:
        image_extension = image.filename.split(".")[-1]
        if image_extension.lower() not in ["jpg", "jpeg", "png"]:
            raise HTTPException(status_code=400, detail="Faqat JPEG va PNG formatlariga ruxsat bor.")
    
    if sertificate:
        sertificate_extension = sertificate.filename.split(".")[-1]
        if sertificate_extension not in ["pdf"]:
            raise HTTPException(status_code=400, detail="Faqat PDF formatlariga ruxsat bor.")


    db_building = Building(**building.model_dump())
    db.add(db_building)
    await db.commit()
    await db.refresh(db_building)


    if image:
        image_path = Path(MEDIA_DIR) / f"building_{db_building.id}_image.{image_extension}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        db_building.image = str(image_path)

    if sertificate:
        sertificate_path = Path(MEDIA_DIR) / f"building_{db_building.id}_sertificate.{sertificate_extension}"
        with open(sertificate_path, "wb") as buffer:
            shutil.copyfileobj(sertificate.file, buffer)
        db_building.sertificate = str(sertificate_path)

    await db.commit()
    await db.refresh(db_building)
    return BuildingResponse.model_validate(db_building)  




async def reads_building(db : AsyncSession) -> list[BuildingResponse]:
    result = await db.execute(select(Building))
    buildings = result.scalars().all()
    return [BuildingResponse.model_validate(building) for building in buildings]



async def read_building(building_id : int , db: AsyncSession) -> BuildingResponse:
    db_building = await db.get(Building, building_id)
    if db_building is None:
        raise HTTPException(status_code=404 , detail="Building not found")
    return BuildingResponse.model_validate(db_building)



async def delete_building(building_id : int , db : AsyncSession) -> dict:
    db_building = await db.get(Building, building_id)
    if db_building is None:
        raise HTTPException(status_code=404 , detail="Building not found")
    await db.delete(db_building)
    await db.commit()
    return None
