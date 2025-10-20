import allure
import requests
import pytest
from data.urls import orders_url
from data.order_data import order_payload

class TestAcceptOrder:
    @allure.title("Корректный ответ сервера при успешном запросе API")
    def test_accept_order_response_success(self, new_courier):
        courier_id = new_courier["id"]
        
        with allure.step("Создаем новый заказ"):
            create_response = requests.post(orders_url, json=order_payload)
            order_track = create_response.json()["track"]
                  
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
    def test_accept_order_without_id(self, new_courier, missing_id):
        courier_id = new_courier["id"]
        
        with allure.step("Создаем новый заказ"):
            create_response = requests.post(orders_url, json=order_payload)
            order_track = create_response.json()["track"]
             
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
    
    @allure.title("Ошибка при принятии заказа с несуществующим id курьера")
    def test_accept_order_with_invalid_courier_id(self, new_courier):
        courier_id = new_courier["id"]

        with allure.step("Создаем новый заказ"):
            create_response = requests.post(orders_url, json=order_payload)
            order_track = create_response.json()["track"]

        with allure.step("Получаем id заказа по его track-номеру"):
            response_get = requests.get(f"{orders_url}/track?t={order_track}")
            order_id = response_get.json()["order"]["id"]

        with allure.step("Отправляем запрос с неверным id курьера"):
            response = requests.put(f"{orders_url}/accept/{order_id}?courierId=999999")

        with allure.step("Проверяем код и сообщение ошибки"):
            assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"
            assert "Курьера с таким id не существует" in response.json().get("message", "")


    @allure.title("Ошибка при принятии заказа с несуществующим id заказа")
    def test_accept_order_with_invalid_order_id(self, new_courier):
        courier_id = new_courier["id"]

        with allure.step("Отправляем запрос с неверным id заказа"):
            response = requests.put(f"{orders_url}/accept/999999?courierId={courier_id}")

        with allure.step("Проверяем код и сообщение ошибки"):
            assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"
            assert "Заказа с таким id не существует" in response.json().get("message", "")
