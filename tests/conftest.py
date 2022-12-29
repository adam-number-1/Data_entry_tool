import pytest
from de_tool.gui import create_app

@pytest.fixture(scope="module")
def pyqt_app():
    app = create_app()
    yield app
    del app
