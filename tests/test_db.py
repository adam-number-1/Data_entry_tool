import pytest
from de_tool.db_model import Apartment

class TestDB:
    def test_get_objects(self):
        list_ = Apartment.get_objects()

    
