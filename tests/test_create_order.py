import allure
import requests
import pytest

class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цвета самоката")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ])

    def test_create_order_with_different_colors(self, orders_url, color):
        
        with allure.step("Формируем тело запроса"):
            payload = {
                "firstName": "Naruto",
                "lastName": "Uchiha",
                "address": "Konoha, 142 apt.",
                "metroStation": 4,
                "phone": "+7 800 355 35 35",
                "rentTime": 5,
                "deliveryDate": "2025-10-13",
                "comment": "Saske, come back to Konoha",
            }
            if color is not None:
                payload["color"] = color

        with allure.step(f"Отправляем POST-запрос на создание заказа (цвет: {color})"):
            response = requests.post(orders_url, json=payload)

        with allure.step("Проверяем успешный ответ"):
            assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"
            body = response.json()
            assert "track" in body, "В ответе нет ключа 'track'"
            assert isinstance(body["track"], int), "Поле 'track' должно быть числом"
