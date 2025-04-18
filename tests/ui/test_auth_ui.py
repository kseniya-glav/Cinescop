from playwright.sync_api import Page, expect
from pages.auth_page import RegistrationPage
import pytest
import allure

@allure.epic("Тестирование входа пользователя")
@allure.feature("Тестирование регистрации, авторизации и аутентификации пользователя")
@pytest.mark.authUI
class TestAuthUI:
      
    @allure.title("Тест на регистрацию и авторизацию пользователя.")
    def test_reg_auth(self, page: Page, registration_user_data):
        reg = RegistrationPage(page)
        reg.go_form_registration()
        reg.fill_form_registration(registration_user_data.fullName, 
                                   registration_user_data.email, 
                                   registration_user_data.password)
        reg.submit_registration()
        reg.wait_for_login_page()
        expect(reg.is_confirmation_message_visible()).to_be_visible()
        reg.fill_form_entry(registration_user_data.email, 
                            registration_user_data.password)
        reg.submit_entry()
        expect(reg.is_logged_message_visible()).to_be_visible()
        