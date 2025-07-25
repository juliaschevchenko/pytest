import pytest

@pytest.fixture(scope="session")
def base_url():
    return "https://reqres.in/api"

@pytest.fixture(scope="session")
def headers():
    return {
        "x-api-key": "reqres-free-v1"
    }
