import pytest

@pytest.mark.smoke
def test_demo1():
    assert 1 == 1, "Didn't match"

@pytest.mark.regression
def test_demo2():
    assert 'a' == 'A', "Didn't match"

@pytest.mark.skip
def test_add_info():
    assert 'testing' == 'testing', "Didn't match"   
    