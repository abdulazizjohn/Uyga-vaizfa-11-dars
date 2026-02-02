from typing import Optional
from sqlalchemy import String , ForeignKey
from sqlalchemy.orm import Mapped , mapped_column , relationship
from database import Base


class Company(Base):
    __tablename__ = "companys"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(50))
    info : Mapped[Optional[str]] = mapped_column(String(150) , nullable=True)
    adres : Mapped[Optional[str]] = mapped_column(String(150) , nullable=True)  
    phone_number : Mapped[str] = mapped_column(String(13) , nullable=True)
    buildings : Mapped[list[Building]] = relationship(back_populates="company")
        

class Building(Base):
    __tablename__ = "buildings"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(155))
    adres : Mapped[Optional[str]] = mapped_column(nullable= True)
    image: Mapped[Optional[str]] = mapped_column(nullable=True)
    sertificate: Mapped[Optional[str]] = mapped_column(nullable=True)
    company_id : Mapped[int] = mapped_column(ForeignKey("companys.id"))
    company : Mapped[Company] = relationship(back_populates="buildings")
    