import pytest
import random
import string

@pytest.fixture
def base_url():
    return "https://qa-scooter.praktikum-services.ru/api/v1"

@pytest.fixture
def courier_url(base_url):
    return f"{base_url}/courier"

@pytest.fixture
def orders_url(base_url):
    return f"{base_url}/orders"

@pytest.fixture
def random_credentials():
    def _generate(n=10):
        return ''.join(random.choices(string.ascii_lowercase, k=n))
    return _generate
