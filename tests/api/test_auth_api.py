from models.db_model import UserDBModel
from models.user_model import UserRegistrResponse, UserLoginResponse
from utils.data_generator import DataGenerator
import pytest
import allure

@allure.epic("Тестирование входа пользователя")
@allure.feature("Тестирование регистрации, авторизации и аутентификации пользователя")
@pytest.mark.authAPI
class TestAuthAPI:

    @allure.title("Тест на регистрацию пользователя.")
    def test_register_user(self, api_manager, registration_user_data):
        response = api_manager.auth_api.register_user(registration_user_data)
        register_user_response = UserRegistrResponse(**response.json())
        assert register_user_response.email == registration_user_data.email, "Email не совпадает"

    @allure.title("Тест на регистрацию и авторизацию пользователя.")
    def test_successfull_login(self, api_manager, registered_user):
        response = api_manager.auth_api.login_user(registered_user, expected_status=[200,201])
        login_user_response = UserLoginResponse(**response.json())
        assert login_user_response.user.email == registered_user.email, "Email не совпадает"

    @allure.title("Тест на неправильный пароль.")
    def test_invalid_password(self, api_manager, registered_user):
        registered_user.password =  DataGenerator.generate_random_password()
        response = api_manager.auth_api.login_user(registered_user, expected_status=401)
        assert "error" in response.json(), "Ответ не содержит сообщения об ошибке"

    @allure.title("Тест на неправильный email.")
    def test_invalid_email(self, api_manager, registered_user):
        registered_user.password =  DataGenerator.generate_random_email()
        response = api_manager.auth_api.login_user(registered_user, expected_status=401)
        assert "error" in response.json(), "Ответ не содержит сообщения об ошибке"

    @allure.title("Тест на пустое тело запроса.")
    def test_invalid_empty_body(self, api_manager):
        login_data = {}
        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        assert "error" in response.json(), "Ответ не содержит сообщения об ошибке"
        
    @allure.title("Тест на регистрацию пользователя с проверкой в базе данных.")
    def test_register_user_db_session(self, api_manager, test_user, db_session):
        response = api_manager.auth_api.register_user(test_user)
        register_user_response = UserRegistrResponse(**response.json())
        users_from_db = db_session.query(UserDBModel).filter(UserDBModel.id == register_user_response.id)
        assert users_from_db.count() == 1, "обьект не попал в базу данных"
        user_from_db = users_from_db.first()
        assert user_from_db.email == test_user.email, "Email не совпадает"