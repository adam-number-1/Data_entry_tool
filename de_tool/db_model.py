from __future__ import annotations
from typing import List, Any

import os
from dotenv import load_dotenv

load_dotenv()

DIALECT = os.environ.get("DIALECT")
DB_USERNAME = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("PASSWORD")
LINK = os.environ.get("LINK")
NAME_OF_DB = os.environ.get("NAME_OF_DB")

import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Connect to the database
engine = sa.create_engine(f"{DIALECT}://{DB_USERNAME}:{PASSWORD}@{LINK}/{NAME_OF_DB}")

# Reflect the existing table
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create a class for the table
BaseApartment = Base.classes.apt_sales_data

# Create a session to query the table
session = Session(engine)

class Apartment: # sqlalchemy doesn¨t like tables with no PK
    #here will be all the columns

    def __init__(self, entry: BaseApartment) -> None:
        self.entry = entry

    @classmethod
    def get_objects(cls) -> List[Apartment]:
        list_of_objects = session.query(BaseApartment).filter(BaseApartment.apt.is_(None)).all()
        list_of_objects = [Apartment(entry) for entry in list_of_objects]
        return list_of_objects

    def get(self, attr_name: str) -> Any:
        """Returns an object attribute given its name"""
        return self.entry.__getattribute__(attr_name)

    def set(self, attr_name: str, value: Any) -> None:
        """Sets the attribute of an object"""
        self.entry.__setattr__(attr_name, value)

if __name__ == "__main__":
    apt = session.query(Apartment).first()
    print("done")