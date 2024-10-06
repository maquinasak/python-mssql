import pytest

from app import app

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    def saliendo():
        print("saliendo")
    request.addfinalizer(saliendo)
    return client

class Test_Usuarios:
    @classmethod
    def setup_class(cls):
        print("\nsetup class")

    @classmethod
    def teardown_class(cls):
        print("\nteardown class")

    def setup_method(self, method):
        if method==self.test1:
            print("\nsetting up test1")
        elif method == self.test2:
            print("\nsetting up test 2")
        elif method == self.test3:
            print("\nsetting up test 3")
        else:
            print("\nsettin up noencontrado")

    def teardown_method(self, method):
        if method==self.test1:
            print("\nteardown  test1")
        elif method == self.test2:
            print("\nteardown test 2")
        elif method == self.test3:
            print("\nteardown test 3")
        else:
            print("\nteardown  no encontrado")

    def test1(self):
        print("test 1")
        assert True

    def test2(self):
        print("test 2")
        assert True

    def test3(self):
        print("test 3")
        assert True
