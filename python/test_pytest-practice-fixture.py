import pytest

@pytest.fixture(scope="function")
def api_client():
    a = [1]
    yield a
    print("teardown")
    del a

def test_api_client(api_client):
    api_client[0] += 2
    assert api_client[0] == 3

def test_api_client_2(api_client):
    assert api_client[0] == 3  # this will fail because the fixture is not reset. if we use scope="session", it will pass.



