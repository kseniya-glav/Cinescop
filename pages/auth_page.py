from constants.const import DEV_CINESCOPE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT

class RegistrationPage:
    
    USERNAME_LOCATOR = '[name="fullName"]'
    EMAIL_LOCATOR = '[name="email"]'
    PASSWORD_LOCATOR = '[name="password"]'
    REPEAT_PASSWORD_LOCATOR = '[placeholder="Повторите пароль"]'
    SUBMIT_REGISTRATION = 'button[type="submit"]:has-text("Зарегистрироваться")'
    SUBMIT_ENTRY = 'button[type="submit"]:has-text("Войти")'

    URL_REGISTR = DEV_CINESCOPE_URL + REGISTER_ENDPOINT
    URL_LOGIN = DEV_CINESCOPE_URL + LOGIN_ENDPOINT
    
    def __init__(self, page):
        self.page = page
        
    def go_form_registration(self):
        self.page.goto(DEV_CINESCOPE_URL + REGISTER_ENDPOINT)   
     
    def fill_form_registration(self, username, user_email, user_password):
        self.page.fill(self.USERNAME_LOCATOR, username)
        self.page.fill(self.EMAIL_LOCATOR, user_email)
        self.page.fill(self.PASSWORD_LOCATOR, user_password)
        self.page.fill(self.REPEAT_PASSWORD_LOCATOR, user_password)

    def submit_registration(self):
        self.page.click(self.SUBMIT_REGISTRATION)
          
    def wait_for_login_page(self):
        self.page.wait_for_url(DEV_CINESCOPE_URL + LOGIN_ENDPOINT)
         
    def is_confirmation_message_visible(self) -> bool:
        return self.page.get_by_text("Подтвердите свою почту")
    
    def fill_form_entry(self, user_email, user_password):
        self.page.fill(self.EMAIL_LOCATOR, user_email)
        self.page.fill(self.PASSWORD_LOCATOR, user_password)
        
    def submit_entry(self):
        self.page.click(self.SUBMIT_ENTRY)
          
    def is_logged_message_visible(self) -> bool:
        return self.page.get_by_text("Вы вошли в аккаунт")
    