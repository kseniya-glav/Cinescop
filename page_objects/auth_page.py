from playwright.sync_api import Page
from constants.const import DEV_CINESCOPE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from page_objects.base_page import BasePage
    
    # USERNAME_LOCATOR = '[name="fullName"]'
    # EMAIL_LOCATOR = '[name="email"]'
    # PASSWORD_LOCATOR = '[name="password"]'
    # REPEAT_PASSWORD_LOCATOR = '[placeholder="Повторите пароль"]'
    # SUBMIT_REGISTRATION = 'button[type="submit"]:has-text("Зарегистрироваться")'
    # SUBMIT_ENTRY = 'button[type="submit"]:has-text("Войти")'
    
class CinescopRegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = self.home_url+REGISTER_ENDPOINT

        # Локаторы элементов        
        self.full_name_input = "input[name='fullName']"
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.repeat_password_input = "input[name='passwordRepeat']"

        self.register_button = 'button[type="submit"]:has-text("Зарегистрироваться")'
        self.sign_button = "a[href='/login' and text()='Войти']"
        
    # Локальные action методы 
    def open(self):
        self.open_url(self.url)

    def register(self, full_name: str, email: str, password: str, confirm_password: str):
        self.enter_text_to_element(self.full_name_input, full_name)
        self.enter_text_to_element(self.email_input, email)
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.repeat_password_input, confirm_password)

        self.click_element(self.register_button)

    def assert_was_redirect_to_login_page(self):
        self.wait_redirect_for_url(self.home_url+LOGIN_ENDPOINT)

    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Подтвердите свою почту")


class CinescopLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = self.home_url+LOGIN_ENDPOINT

        # Локаторы элементов        
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"

        self.login_button = 'button[type="submit"]:has-text("Войти")'
        self.register_button = "a[href='/register' and text()='Зарегистрироваться']"
    
    # Локальные action методы 
    def open(self):
        self.open_url(self.url)

    def login(self, email: str, password: str):
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.email_input, email)
        self.click_element(self.login_button)

    def assert_was_redirect_to_home_page(self):
        self.wait_redirect_for_url(self.home_url)

    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Вы вошли в аккаунт")