from models.user_model import UserRegistrResponse
import pytest
import allure

@allure.epic("Тестирование сущности пользователь")
@allure.feature("Тестирование crud-операций")
@pytest.mark.userAPI
class TestUserAPI:
    
    @allure.title("Тест на создание пользователя")
    def test_create_user(self, super_admin, creation_user_data):
        with allure.step("Создаем пользователя"):
            create_user_response = UserRegistrResponse(**super_admin.api.user_api.create_user(creation_user_data).json())
        with allure.step("Проверяем email в ответе запроса"):
            assert create_user_response.email == creation_user_data.email, "Email не совпадает"

    @allure.title("Тест на поиск пользователя по id и email")
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        with allure.step("Создаем пользователя"):
            create_user_response = UserRegistrResponse(**super_admin.api.user_api.create_user(creation_user_data).json())
        with allure.step("Поиск пользователя по id и email"):
            response_by_id = UserRegistrResponse(**super_admin.api.user_api.get_user(create_user_response.id).json())
            response_by_email = UserRegistrResponse(**super_admin.api.user_api.get_user(create_user_response.email).json())
        with allure.step("Проверяем идентичность ответов на запрос по id и по email"):
            assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        
    @allure.title("Тест на получение данных пользователя по email, без права доступа")
    def test_get_user_by_id_common_user(self, common_user):
        with allure.step("Пробуем получить данные о пользователя, не имея на это прав"):
            common_user.api.user_api.get_user(common_user.email, expected_status=403)
 