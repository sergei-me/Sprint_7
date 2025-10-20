import pytest
import requests
from helpers.courier_generator import register_new_courier_and_return_login_password
from data import urls

@pytest.fixture
def new_courier():
    login, password, first_name = register_new_courier_and_return_login_password(urls.courier_url)
    
    payload = {"login": login, "password": password}
    response = requests.post(f"{urls.courier_url}/login", json=payload)
    courier_id = response.json().get("id")
    
    courier_data = {
        "login": login,
        "password": password,
        "first_name": first_name,
        "id": courier_id
    }
    
    yield courier_data

    if courier_id:
        requests.delete(f"{urls.courier_url}/{courier_id}")

