from models.user_model import UserRegistrResponse

class TestUserAPI:
    
    def test_create_user(self, super_admin, creation_user_data):
        """Тест на создание пользователя."""
        create_user_response = UserRegistrResponse(**super_admin.api.user_api.create_user(creation_user_data).json())
        assert create_user_response.email == creation_user_data.email, "Email не совпадает"

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        """Тест на поиск пользователя по id и email"""
        create_user_response = UserRegistrResponse(**super_admin.api.user_api.create_user(creation_user_data).json())
        response_by_id = UserRegistrResponse(**super_admin.api.user_api.get_user(create_user_response.id).json())
        response_by_email = UserRegistrResponse(**super_admin.api.user_api.get_user(create_user_response.email).json())
        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        
    def test_get_user_by_id_common_user(self, common_user):
        """Тест на получение данных пользователя по email, без права доступа"""
        common_user.api.user_api.get_user(common_user.email, expected_status=403)
 