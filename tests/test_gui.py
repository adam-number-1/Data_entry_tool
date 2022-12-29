import pytest
from unittest.mock import *

from de_tool.gui import create_app, QApplication, MainWindow, ObjectTable

@pytest.mark.usefixtures("pyqt_app")
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

@pytest.mark.usefixtures("pyqt_app")
class TestObjectTable:

    @pytest.fixture
    def test_table(self):
        return ObjectTable()

    def test_init(self, pyqt_app, test_table):
        assert not test_table.object_list 
        assert not test_table.INGORE_AUTO_COMMIT

    def test_add_list(self, pyqt_app, test_table):
        test_table.add_list(["a","b","c"])
        assert test_table.object_list == ["a","b","c"]

    def create_table_from_obj_list(self, pyqt_app):
        test_table = ObjectTable.create_table_from_obj_list(["a","b","c"])
        assert test_table.object_list == ["a","b","c"]

    @pytest.fixture
    def object_dicts(self):
        list_of_attr = ["id", "district", "street", "number", "house", "apt", "furnished"]

        def return_dict(list_of_vals):
            d = {}
            for n,val in enumerate(list_of_vals):
                d[list_of_attr[n]] = val
        
            return d
        d1 = return_dict([11]+["1"+str(n) for n in range(2,8)])
        d2 = return_dict([21]+["2"+str(n) for n in range(2,8)])
        d3 = return_dict([31]+["3"+str(n) for n in range(2,8)])
        return [d1,d2,d3]

    def test_draw_table(self, pyqt_app, object_dicts):
        test_table = ObjectTable.create_table_from_obj_list(object_dicts)
        test_table.draw_table()

        assert not test_table.INGORE_AUTO_COMMIT
        header = [test_table.horizontalHeaderItem(n).text() for n in range(len(test_table.attributes))]
        assert header == test_table.attributes

        assert test_table.rowCount() == len(object_dicts)
        assert test_table.columnCount() == len(test_table.attributes)

        for n in range(3):
            for m in range(7):

                if m == 1:
                    # test_table.itemAt(n-1,m-1).flags()
                    pass

                assert test_table.item(n,m).text() == str(object_dicts[n][test_table.attributes[m]])

    @pytest.fixture
    def test_lists(self, object_dicts):
        return ([], object_dicts)

    @patch('de_tool.gui.session.delete')
    def test_delete_row(self, session_mock, test_lists, pyqt_app):
        test_table = ObjectTable.create_table_from_obj_list(test_lists[0])
        test_table.delete_row(1)

        assert not session_mock.called

        session_mock.reset_mock()

        class MockDict:
            def __init__(self, d):
                self.d = d
            
            @property
            def entry(self):
                return self.d

        test_l = [MockDict(_) for _ in test_lists[1]]
        test_table = ObjectTable.create_table_from_obj_list(test_l)

        test_table.delete_row(1)
        session_mock.assert_called_with(test_l[1].entry)

    @patch('de_tool.gui.session.execute')
    def test_blacklist_ad(self,session_execute_mock):
        test_table = ObjectTable()
        obj_list = []

        for n in range(3):
            mock = Mock()
            mock.entry.link = str(n)
            obj_list.append(mock)

        test_table.add_list(obj_list)

        test_table.blacklist_ad(1)
        session_execute_mock.assert_called_with("INSERT INTO sales_blacklist (link) VALUES ('1') ON DUPLICATE KEY UPDATE link = link;")


    def test_update_object_list(self):

        class ListItem(dict):
            def set(self, attr:str, val: int | str) -> None:
                self[attr] = val

            def get(self, attr:str):
                return self[attr]

        keys = ["id", "district", "street", "number", "house", "apt", "furnished"]
        list_of_items = []

        for n in range(3):
            new_values = [n] + [str(n)+_ for _ in "012345"]
            list_of_items.append(ListItem(zip(keys,new_values)))

        list_of_check = []

        for n in range(3,6):
            new_values = [n] + [str(n)+_ for _ in "012345"]
            list_of_check.append(ListItem(zip(keys,new_values)))
        
        tested_table = ObjectTable.create_table_from_obj_list(list_of_items)
        tested_table.draw_table()

        tested_table.add_list(list_of_check)
        tested_table.update_object_list()

        assert tested_table.object_list == list_of_items
        
          

            

