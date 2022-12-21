import pytest

from de_tool import create_app, QApplication, MainWindow

class TestQAPP:

    @pytest.fixture(scope="session")
    def app_fix(self):
        app = QApplication([])
        yield app
        app.quit()
        del app

    def test_create_app(self):
        """This thing tests the main app factory"""
        app = create_app()
        assert type(app) == QApplication

    def test_window_creation(self,app_fix):
        """Tests the creation of the main window"""
        
        app = app_fix

        win = MainWindow()

        assert win.windowTitle() == "Data entry tool"

