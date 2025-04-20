from playwright.sync_api import Page, expect
import pytest
import allure
from page_objects.auth_page import CinescopLoginPage, CinescopRegisterPage
    
@allure.epic("Тестирование UI")
@allure.feature("Тестирование регистрации, авторизации и аутентификации пользователя")
@pytest.mark.ui
class TestAuthUI:
    @allure.title("Тест на регистрацию и авторизацию пользователя.")
    def test_reg_auth(self, page: Page, registration_user_data):
        reg_page = CinescopRegisterPage(page)
        reg_page.open()
        reg_page.register(registration_user_data.fullName, registration_user_data.email, 
                    registration_user_data.password, registration_user_data.password)
        reg_page.assert_was_redirect_to_login_page()  
        reg_page.make_screenshot_and_attach_to_allure() 
        reg_page.assert_allert_was_pop_up() 
        login_page = CinescopLoginPage(page)
        login_page.open()       
        login_page.login(registration_user_data.email, registration_user_data.password) 
        login_page.assert_was_redirect_to_home_page() 
        login_page.make_screenshot_and_attach_to_allure() 
        login_page.assert_allert_was_pop_up() 

        
@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestloginPage:
    @allure.title("Проведение успешного входа в систему")
    def test_login_by_ui(self, page: Page, registered_user):
        login_page = CinescopLoginPage(page)
        login_page.open()       
        login_page.login(registered_user.email, registered_user.password) 
        login_page.assert_was_redirect_to_home_page() 
        login_page.make_screenshot_and_attach_to_allure() 
        login_page.assert_allert_was_pop_up() 
        
        
@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:      
    @allure.title("Проведение успешной регистрации")
    def test_register_by_ui(self, page: Page, registration_user_data):
        email = registration_user_data.email
        name = registration_user_data.fullName
        password = registration_user_data.password
        register_page = CinescopRegisterPage(page) 
        register_page.open()
        register_page.register(f"PlaywrightTest {name}", email, password, password)
        register_page.assert_was_redirect_to_login_page()  
        register_page.make_screenshot_and_attach_to_allure() 
        register_page.assert_allert_was_pop_up() 
