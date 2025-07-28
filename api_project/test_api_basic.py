import requests
import pytest

def test_get_users(base_url, headers):
    response = requests.get(f"{base_url}/users?page=2", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'data' in data
    assert isinstance(data["data"], list)

def test_create_user(base_url, headers):

    payload = {
        "name": "Юля",
        "job": "QA Engineer"
    }

    response = requests.post(f"{base_url}/users", json=payload, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Юля"
    assert data["job"] == "QA Engineer"
    assert "id" in data
    assert "createdAt" in data

def test_update_user(base_url, headers):
    payload = {
        "name": "Юля",
        "job": "Lead QA"
    }

    response = requests.put(f"{base_url}/users/2", json=payload, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Юля"
    assert data["job"] == "Lead QA"
    assert "updatedAt" in data

def test_delete_user(base_url, headers):
    response = requests.delete(f"{base_url}/users/2", headers=headers)
    assert response.status_code == 204  # Нет содержимого, но успешно

@pytest.mark.xfail(reason="баг на стороне API")
def test_create_user_without_body(base_url, headers):
    response = requests.post(f"{base_url}/users", headers=headers)
    assert response.status_code == 400 or response.status_code == 415  # зависит от API

def test_get_nonexistent_resource(base_url, headers):
    response = requests.get(f"{base_url}/unknown/999", headers=headers)
    assert response.status_code == 404

@pytest.mark.xfail(reason="reqres.in может возвращать 200 с некорректным API-ключом")
def test_with_invalid_api_key(base_url):
    headers = {"x-api-key": "invalid-key"}
    response = requests.get(f"{base_url}/users/2", headers=headers)
    assert response.status_code == 401
