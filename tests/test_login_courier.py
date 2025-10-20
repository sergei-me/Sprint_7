import allure
import requests
import pytest
from helpers.courier_generator import register_new_courier_and_return_login_password
from helpers.helpers import random_string
from data.urls import login_url, courier_url

class TestLoginCourier:
    
    @allure.title("Авторизация курьера успешна")
    def test_login_courier_success(self):
        with allure.step("Регистрация нового курьера через API"):
            login_pass = register_new_courier_and_return_login_password(courier_url)
            login, password, first_name = login_pass
        
        with allure.step("Авторизация созданным курьером"):
            payload = {"login": login, "password": password}
            response = requests.post(login_url, json=payload)
        
        with allure.step("Проверяем успешный ответ"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
            assert "id" in response.json(), "В ответе нет id курьера"
    
    @allure.title("Авторизация незарегистрированного курьера")
    def test_unregistration_courier(self):
        with allure.step("Генирируем случайную пару логин/пароль"):
            login = random_string()
            password = random_string()

        with allure.step("Авторизация созданным курьером"):
            payload = {"login": login, "password": password}
            response = requests.post(login_url, json=payload)
        
        with allure.step("Проверяем ошибку в ответе"):
            assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"
            assert "Учетная запись не найдена" in response.json().get("message", "")
    
    @allure.title("Ошибка авторизации курьера без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_courier_missing_field(self, missing_field):
        with allure.step("Генирируем случайную пару логин/пароль"):
            login = random_string()
            password = random_string()
            payload = {"login": login, "password": password}
            payload.pop(missing_field)
        
        with allure.step(f"Попытка авторизоваться без обязательного поля: {missing_field}"):
            response = requests.post(login_url, json=payload)

        with allure.step("Проверяем ошибку в ответе"):
            # Тест правильный, в работе сервера баг, по согласованию с наставником пишем с комментом
            # Сервер неправильно обпрабатывает запрос без пароля
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
            assert "Недостаточно данных для входа" in response.json().get("message", "")
    
    @allure.title("Ошибка при авторизации с неверным логином или паролем")
    @pytest.mark.parametrize("field_to_change", ["login", "password"])
    def test_login_courier_wrong_credentials(self, field_to_change):
        with allure.step("Регистрация нового курьера через API"):
            login_pass = register_new_courier_and_return_login_password(courier_url)
            login, password, first_name = login_pass

        with allure.step(f"Изменяем {field_to_change} на неверное значение"):
            wrong_login = random_string()
            wrong_password = random_string()

            payload = {
                "login": wrong_login if field_to_change == "login" else login,
                "password": wrong_password if field_to_change == "password" else password
            }

        with allure.step("Пробуем авторизоваться с неверными данными"):
            response = requests.post(login_url, json=payload)

        with allure.step("Проверяем ошибку в ответе"):
            assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"
            assert "Учетная запись не найдена" in response.json().get("message", "")
