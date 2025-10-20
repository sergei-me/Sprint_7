import allure
import requests
from data.urls import orders_url
from data.order_data import order_payload

class TestOrderByNumber:
    @allure.title('Успешное получение заказа по номеру')
    def test_get_order_by_number_success(self):
        
        with allure.step("Создаем новый заказ"):
            create_response = requests.post(orders_url, json=order_payload)
            order_track = create_response.json()["track"]
        
        with allure.step("Получение заказа по номеру"):
            response = requests.get(f"{orders_url}/track?t={order_track}")
        
        with allure.step("Проверяем успешный ответ сервера и получение объекта"):
            assert response.status_code == 200, f"Ожидался 200, получен {create_response.status_code}"
            assert response.json().get("order") is not None
    
    @allure.title('Ошибка при оправке запроса без track-номера')
    def test_get_order_by_number_without_track(self):
        with allure.step("Получение заказа по номеру"):
            response = requests.get(f"{orders_url}/track?t=")
        
        with allure.step("Проверяем кода ответа и тела ошибки"):
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
            assert "Недостаточно данных для поиска" in response.json().get("message", "")   

    @allure.title('Ошибка при оправке запроса с несуществующим track-номером')
    def test_get_order_by_number_invalid_track(self):
        with allure.step("Получение заказа по номеру"):
            response = requests.get(f"{orders_url}/track?t=999999")
        
        with allure.step("Проверяем кода ответа и тела ошибки"):
            assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"
            assert "Заказ не найден" in response.json().get("message", "")
