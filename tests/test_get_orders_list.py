import allure
import requests

class TestOrderList:

    @allure.title("Получение списка заказов")
    @allure.description("Проверяем, что в ответе возвращается список заказов")
    def test_get_orders_list(self, orders_url):

        with allure.step("Отправляем GET-запрос на получение списка заказов"):
            response = requests.get(orders_url)

        with allure.step("Проверяем, что сервер вернул 200 OK"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        with allure.step("Проверяем, что тело ответа содержит список заказов"):
            body = response.json()
            assert "orders" in body, "В ответе отсутствует ключ 'orders'"
            assert isinstance(body["orders"], list), "Поле 'orders' должно быть списком"
