from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI , Depends, Form, UploadFile
from fastapi.staticfiles import StaticFiles
import uvicorn
from database import Base ,  engine , get_db, MEDIA_DIR
from schemas import * 
import crud


app = FastAPI()
app.mount(f"/{MEDIA_DIR}", StaticFiles(directory="media"), name="media")

async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        


@app.on_event("startup")
async def startup_event():
    await init_db()
    
@app.get("/company",response_model=list[CompanyResponse])
async def read_companys(db:AsyncSession = Depends(get_db)):
    return await crud.reads_company(db)


@app.post("/company",response_model=CompanyResponse)
async def create_company_end(company  : CompanyCreate, db:AsyncSession = Depends(get_db)):
    return await crud.create_company(company, db)


@app.get("/company/{company_id}",response_model=CompanyResponse)
async def read_company(company_id : int ,db:AsyncSession = Depends(get_db)):
    return await crud.read_company(company_id , db)


@app.put("/company/{company_id}",response_model=CompanyResponse)
async def update_company(company_id : int, company  : CompanyCreate ,db:AsyncSession = Depends(get_db)):
    return await crud.update_company(company_id, company , db)


@app.delete("/company/{company_id}",response_model=None, status_code=204)
async def delete_company(company_id : int ,db:AsyncSession = Depends(get_db)):
    return await crud.delete_company(company_id , db)



@app.post("/building",response_model=BuildingResponse)
async def create_building_endpoint(
    name: str = Form(...),
    adres: str = Form(...),
    company_id: int = Form(...),
    image: UploadFile = None,
    sertificate: UploadFile = None,
    db: AsyncSession = Depends(get_db)
):
    building_data = BuildingCreate(
        name=name,
        adres=adres,
        company_id=company_id
    )
    return await crud.create_building(building_data, db, image, sertificate)        

@app.get("/buildings",response_model=list[BuildingResponse])
async def read_buildings(db:AsyncSession = Depends(get_db)):
    return await crud.reads_building(db)

@app.get("/building/{building_id}",response_model=BuildingResponse)
async def read_building(building_id : int ,db:AsyncSession = Depends(get_db)):
    return await crud.read_building(building_id , db)


@app.delete("/building/{building_id}",response_model=None, status_code=204)
async def delete_building(building_id : int ,db:AsyncSession = Depends(get_db)):
    return await crud.delete_building(building_id , db)


if __name__ == "__main__":
    uvicorn.run(app)