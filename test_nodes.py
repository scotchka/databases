import tempfile
import pytest
from nodes import Filescan, Selection, Projection


@pytest.fixture
def csv():
    with tempfile.NamedTemporaryFile() as f:
        f.write(
            b"""a,b,c
1,2,3
4,5,6
7,8,9
10,11,12"""
        )
        f.seek(0)
        yield f


def test_filescan(csv):

    assert list(Filescan(csv.name)) == [
        ("1", "2", "3"),
        ("4", "5", "6"),
        ("7", "8", "9"),
        ("10", "11", "12"),
    ]


def test_equals(csv):
    assert list(Selection("c", "EQUALS", "6", child=Filescan(csv.name))) == [
        ("4", "5", "6")
    ]


def test_contains(csv):
    assert list(Selection("a", "CONTAINS", "1", child=Filescan(csv.name))) == [
        ("1", "2", "3"),
        ("10", "11", "12"),
    ]


def test_projection(csv):
    assert list(Projection("b", child=Filescan(csv.name))) == [
        ("2",),
        ("5",),
        ("8",),
        ("11",),
    ]
