import allure
import requests
import pytest
from helpers.courier_generator import register_new_courier_and_return_login_password

class TestCreateCourier:

    @allure.title("Курьера можно создать")
    def test_create_courier_success(self, courier_url):
        with allure.step("Регистрация нового курьера через API"):
            login_pass = register_new_courier_and_return_login_password(courier_url)
        
        with allure.step("Проверка, что курьер успешно создан"):
            assert login_pass, "Не удалось создать курьера через API"

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, courier_url):
        with allure.step("Создание первого курьера"):
            login_pass = register_new_courier_and_return_login_password(courier_url)
            login, password, first_name = login_pass
        
        with allure.step("Попытка создать курьера с тем же логином"):
            payload = {"login": login, "password": password, "firstName": first_name}
            response = requests.post(courier_url, json=payload)
        
        with allure.step("Проверка кода ответа и текста ошибки"):
            assert response.status_code == 409, f"Ожидался 409, получен {response.status_code}"
            assert "Этот логин уже используется" in response.json().get("message", "")

    @allure.title("Ошибка при создании курьера без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, courier_url, random_credentials, missing_field):
        login = random_credentials()
        password = random_credentials()
        payload = {"login": login, "password": password}
        payload.pop(missing_field)

        with allure.step(f"Попытка создать курьера без обязательного поля: {missing_field}"):
            response = requests.post(courier_url, json=payload)
        
        with allure.step("Проверка кода ответа и текста ошибки"):
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
            assert "Недостаточно данных для создания учетной записи" in response.json().get("message", "")

    @allure.title("Правильный код ответа при создании курьера")
    def test_create_courier_status_code(self, courier_url, random_credentials):
        login = random_credentials()
        password = random_credentials()
        first_name = random_credentials()
        payload = {"login": login, "password": password, "firstName": first_name}

        with allure.step("Создание нового курьера"):
            response = requests.post(courier_url, json=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 201

    @allure.title("Правильный текст ответа при создании курьера")
    def test_create_courier_response_text(self, courier_url, random_credentials):
        login = random_credentials()
        password = random_credentials()
        first_name = random_credentials()
        payload = {"login": login, "password": password, "firstName": first_name}

        with allure.step("Создание нового курьера"):
            response = requests.post(courier_url, json=payload)

        with allure.step("Проверка текста ответа"):
            assert response.json() == {'ok': True}
