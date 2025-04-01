from models.user_model import UserRegistrResponse, UserLoginResponse
from utils.data_generator import DataGenerator

class TestAuthAPI:

    def test_register_user(self, api_manager, registration_user_data):
        """Тест на регистрацию пользователя."""
        response = api_manager.auth_api.register_user(registration_user_data)
        register_user_response = UserRegistrResponse(**response.json())
        assert register_user_response.email == registration_user_data.email, "Email не совпадает"

    def test_successfull_login(self, api_manager, registered_user):
        """Тест на регистрацию и авторизацию пользователя."""
        response = api_manager.auth_api.login_user(registered_user, expected_status=[200,201])
        login_user_response = UserLoginResponse(**response.json())
        assert login_user_response.user.email == registered_user.email, "Email не совпадает"

    def test_invalid_password(self, api_manager, registered_user):
        """Тест на неправильный пароль."""
        registered_user.password =  DataGenerator.generate_random_password()
        response = api_manager.auth_api.login_user(registered_user, expected_status=401)
        assert "error" in response.json(), "Ответ не содержит сообщения об ошибке"

    def test_invalid_email(self, api_manager, registered_user):
        """Тест на неправильный email."""
        registered_user.password =  DataGenerator.generate_random_email()
        response = api_manager.auth_api.login_user(registered_user, expected_status=401)
        assert "error" in response.json(), "Ответ не содержит сообщения об ошибке"

    def test_invalid_empty_body(self, api_manager):
        """Тест на пустое тело запроса."""
        login_data = {}
        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        assert "error" in response.json(), "Ответ не содержит сообщения об ошибке"
        