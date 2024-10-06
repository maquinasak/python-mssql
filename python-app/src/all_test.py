import os
import pytest
from pytest import approx, raises
from unittest.mock import MagicMock

@pytest.fixture()
def myfixture():
    print("\nMyFixture")


@pytest.fixture(params=[1,2,3])
def client_prueba(request):
    rta = request.param
    return rta

def raisemyexcept(myValue):
    if myValue == 1:
        raise Exception("exception")
    return 0

def test_exception():
    with raises(Exception):
        raisemyexcept(1)


def test_clientprueba(client_prueba):
    print(client_prueba)
    assert True

def test_int():
    assert 1 == 1

def test_float():
    assert (0.2 + 0.159 - 0.159) == approx(0.2)

def test_array():
    assert [1,2,3] == [1,2,3]

def test_dict():
    assert {"1":1} == {"1":1}

def str_len(theStr):
    return len(theStr)

@pytest.mark.usefixtures("myfixture")
def test_string_length():
    caracteres = ["1","ds","tre","cuat","cinco"]    
    for idx,valor in enumerate(caracteres):
        # print(valor,idx,str_len(valor))
        result = str_len(valor)
        assert result == (idx+1)

@pytest.mark.skip
def test_Foo():
    bar = Mock(spec=SpecClass)
    bar2 = Mock(side_effect = barFunc)
    bar3 = Mock(return_value=1)


def readFromFile(nombreArchivo):
    if not os.path.exists(nombreArchivo):
        raise Exception("bad file")
    infile = open(nombreArchivo, "r")
    line = infile.readline()
    return line

@pytest.fixture()
def mock_open(monkeypatch):
    mock_file = MagicMock()
    mock_file.readline = MagicMock(return_value="test line")
    mock_open = MagicMock(return_value=mock_file)
    monkeypatch.setattr("builtins.open", mock_open)
    return mock_open

def test_returnsCorrectMock(mock_open, monkeypatch):
    mock_exists = MagicMock(return_value=True)
    monkeypatch.setattr("os.path.exists", mock_exists)
    result = readFromFile("blaa")
    mock_open.assert_called_once_with("blaa","r")
    assert result == "test line"

def test_returnsCorrectExceptionMock(mock_open, monkeypatch):
    mock_exists = MagicMock(return_value=False)
    monkeypatch.setattr("os.path.exists", mock_exists)
    with raises(Exception):
        result = readFromFile("blaa")
