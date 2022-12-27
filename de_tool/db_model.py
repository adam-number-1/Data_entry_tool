from __future__ import annotations
from typing import List, Any

import os
from dotenv import load_dotenv

load_dotenv()


from sqlalchemy import create_engine, Column, Integer, String, Date, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DIALECT = os.environ.get("DIALECT")
DB_USERNAME = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("PASSWORD")
LINK = os.environ.get("LINK")
NAME_OF_DB = os.environ.get("NAME_OF_DB")

engine = create_engine(f"{DIALECT}://{DB_USERNAME}:{PASSWORD}@{LINK}/{NAME_OF_DB}")

session = sessionmaker(bind=engine)()

base = declarative_base()

class Apartment(base): # sqlalchemy doesn¨t like tables with no PK
    __tablename__ = "apartment_sales_records"

    id = Column(Integer, name="id", primary_key = True)
    link = Column(String(200), name="link")
    district = Column(String(50), name="district")
    shape = Column(String(4), name="shape")


    #here will be all the columns

    @classmethod
    def get_objects(cls) -> List[Apartment]:
        list_of_objects = session.query(cls).filter(cls.shape.is_(None)).all()
        return list_of_objects

    def get(self, attr_name: str) -> Any:
        """Returns an object attribute given its name"""
        return self.__getattribute__(attr_name)

    def set(self, attr_name: str, value: Any) -> None:
        """Sets the attribute of an object"""
        self.__setattr__(attr_name, value)

base.metadata.create_all(engine)

if __name__ == "__main__":
    
    apt1 = {
    "id" : 1,
    "link" : "https://www.sreality.cz/detail/prodej/byt/3+1/praha-vrsovice-moskevska/269964876",
    "district" : "A",
    "shape" : None
    }

    apt2 = {
    "id" : 2,
    "link" : "https://www.sreality.cz/detail/prodej/byt/1+1/praha-stare-mesto-narodni/2712798796",
    "district" : "B",
    "shape" : None
    }

    apt3 = {
    "id" : 3,
    "link" : "https://www.sreality.cz/detail/prodej/byt/2+kk/praha-zizkov-jicinska/3153643868",
    "district" : "C",
    "shape" : None
    }

    
    for apt in [apt1,apt2,apt3]:
        session.merge(Apartment(**apt))
        session.commit()