import allure
import requests
import pytest
from helpers.courier_generator import register_new_courier_and_return_login_password

class TestAcceptOrder:
    @allure.title("Корректный ответ сервера при успешном запросе API")
    def test_accept_order_response_success(self, courier_url, orders_url):
        with allure.step("Регистрация нового курьера через API"):
            login_pass = register_new_courier_and_return_login_password(courier_url)
            login, password, first_name = login_pass
        
        with allure.step("Авторизация созданным курьером"):
            payload = {"login": login, "password": password}
            courier_response = requests.post(f"{courier_url}/login", json=payload)
            courier_id = courier_response.json()["id"]
        
        with allure.step("Создаем новый заказ"):
            order_payload = {
                "firstName": "Naruto",
                "lastName": "Uchiha",
                "address": "Konoha, 142 apt.",
                "metroStation": 4,
                "phone": "+7 800 355 35 35",
                "rentTime": 5,
                "deliveryDate": "2025-10-13",
                "comment": "Saske, come back to Konoha",
                "color": ["BLACK"]
            }

            create_response = requests.post(orders_url, json=order_payload)
            order_track = create_response.json()["track"]
        
        with allure.step("Проверка успешного создания заказа"):
            assert create_response.status_code == 201, f"Ожидался 201, получен {create_response.status_code}"
            
        with allure.step("Получаем id заказа по его track-номеру"):
            response_get = requests.get(f"{orders_url}/track?t={order_track}")
            order_id = response_get.json()["order"]["id"]
        
        with allure.step("Принимаем заказ"):
            response = requests.put(f"{orders_url}/accept/{order_id}?courierId={courier_id}")

        with allure.step("Проверяем успешное принятие заказа"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
            assert response.json() == {"ok": True}

    @allure.title("Ошибка при принятии заказа без id курьера или заказа")
    @pytest.mark.parametrize("missing_id", ["courier_id", "order_id"])
    def test_accept_order_without_id(self, courier_url, orders_url, missing_id):
        with allure.step("Регистрация нового курьера через API"):
            login_pass = register_new_courier_and_return_login_password(courier_url)
            login, password, first_name = login_pass
        
        with allure.step("Авторизация созданным курьером"):
            payload = {"login": login, "password": password}
            courier_response = requests.post(f"{courier_url}/login", json=payload)
            courier_id = courier_response.json()["id"]
        
        with allure.step("Создаем новый заказ"):
            payload = {
                "firstName": "Naruto",
                "lastName": "Uchiha",
                "address": "Konoha, 142 apt.",
                "metroStation": 4,
                "phone": "+7 800 355 35 35",
                "rentTime": 5,
                "deliveryDate": "2025-10-13",
                "comment": "Saske, come back to Konoha",
                "color": ["BLACK"]
            }

            create_response = requests.post(orders_url, json=payload)
            order_track = create_response.json()["track"]
        
        with allure.step("Проверка успешного создания заказа"):
            assert create_response.status_code == 201, f"Ожидался 201, получен {create_response.status_code}"
            
        with allure.step("Получаем id заказа по его track-номеру"):
            response_get = requests.get(f"{orders_url}/track?t={order_track}")
            order_id = response_get.json()["order"]["id"]
        
        with allure.step("Формируем некорректный запрос принятия заказа"):
            if missing_id == "courier_id":
                response = requests.put(f"{orders_url}/accept/{order_id}")
            else:
                response = requests.put(f"{orders_url}/accept/?courierId={courier_id}")
        # При отсутствии order_id сервер выдает неправильный ответ 404 - это несоответствует Api Doc - баг
        with allure.step("Проверка кода ответа и текста ошибки"):
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
            assert "Недостаточно данных для поиска" in response.json().get("message", "")
    
    @allure.title("Ошибка при принятии заказа с неверным id курьера или заказа")
    @pytest.mark.parametrize("invalid_id_type", ["courier_id", "order_id"])
    def test_accept_order_with_invalid_id(self, courier_url, orders_url, invalid_id_type):
        with allure.step("Регистрация нового курьера через API"):
            login_pass = register_new_courier_and_return_login_password(courier_url)
            login, password, first_name = login_pass

        with allure.step("Авторизация созданным курьером"):
            payload = {"login": login, "password": password}
            courier_response = requests.post(f"{courier_url}/login", json=payload)
            courier_id = courier_response.json()["id"]

        with allure.step("Создаем новый заказ"):
            order_payload = {
                "firstName": "Naruto",
                "lastName": "Uchiha",
                "address": "Konoha, 142 apt.",
                "metroStation": 4,
                "phone": "+7 800 355 35 35",
                "rentTime": 5,
                "deliveryDate": "2025-10-13",
                "comment": "Saske, come back to Konoha",
                "color": ["BLACK"]
            }

            create_response = requests.post(orders_url, json=order_payload)
            order_track = create_response.json()["track"]
        
        with allure.step("Проверка успешного создания заказа"):
            assert create_response.status_code == 201, f"Ожидался 201, получен {create_response.status_code}"

        with allure.step("Получаем id заказа по его track-номеру"):
            response_get = requests.get(f"{orders_url}/track?t={order_track}")
            order_id = response_get.json()["order"]["id"]

        with allure.step("Формируем некорректный запрос принятия заказа"):
            if invalid_id_type == "courier_id":
                response = requests.put(f"{orders_url}/accept/{order_id}?courierId=999999")
            else:
                response = requests.put(f"{orders_url}/accept/999999?courierId={courier_id}")

        with allure.step("Проверяем, что вернулся код 404 и корректное сообщение"):
            assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"
            if invalid_id_type == "courier_id":
                assert "Курьера с таким id не существует" in response.json().get("message", "")
            else:
                assert "Заказа с таким id не существует" in response.json().get("message", "")

