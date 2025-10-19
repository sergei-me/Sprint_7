import allure
import requests
from helpers.courier_generator import register_new_courier_and_return_login_password


class TestDeleteCourier:

    @allure.title("Удаление курьера — успешный сценарий")
    def test_delete_courier_success(self, courier_url):
        with allure.step("Создаем нового курьера через API"):
            login_pass = register_new_courier_and_return_login_password(courier_url)
            login, password, first_name = login_pass

        with allure.step("Получаем id созданного курьера"):
            response = requests.post(f"{courier_url}/login", json={"login": login, "password": password})
            courier_id = response.json()["id"]
      
        with allure.step("Удаляем курьера по его ID"):
            response = requests.delete(f"{courier_url}/{courier_id}", json={"id": courier_id})

        with allure.step("Проверяем успешное удаление"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
            assert response.json() == {"ok": True}
    
    @allure.title("Ошибка при удалении курьера без ID в теле запроса")
    def test_delete_courier_without_id(self, courier_url):
        with allure.step("Создаем нового курьера через API"):
            login_pass = register_new_courier_and_return_login_password(courier_url)
            login, password, first_name = login_pass

        with allure.step("Получаем id созданного курьера"):
            response = requests.post(f"{courier_url}/login", json={"login": login, "password": password})
            courier_id = response.json()["id"]
      
        with allure.step("Удаляем курьера по его id, но не пишем id в теле запроса"):
            response = requests.delete(f"{courier_url}/{courier_id}")

        with allure.step("Проверяем, что вернулась ошибка 400"):
            # Реализовать ошибку 400 сервер не в состоянии, так как он определяет этот запрос без учета тела
            # Выдает 200, если есть ID в url и 404 если нет, что логично
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
            assert "Недостаточно данных для удаления курьера" in response.json().get("message", "")       
    
    @allure.title("Ошибка при удалении несуществующего курьера")
    def test_delete_courier_with_invalid_id(self, courier_url):
        with allure.step("Пробуем удалить курьера с несуществующим id"):
            wrong_courier_id = 999999
            response = requests.delete(f"{courier_url}/{wrong_courier_id}", json={"id": wrong_courier_id})

        with allure.step("Проверяем, что вернулась ошибка 404"):
            assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"
            assert "Курьера с таким id нет" in response.json().get("message", "")

