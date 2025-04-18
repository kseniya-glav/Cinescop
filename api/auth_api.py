from constants.const import REGISTER_ENDPOINT, LOGIN_ENDPOINT, AUTH_DEV_CINESCOPE_URL
from custom_requester.custom_requester import CustomRequester

class AuthAPI(CustomRequester):
    """Класс для работы с аутентификацией."""
    
    def __init__(self, session):
        super().__init__(session= session, base_url = AUTH_DEV_CINESCOPE_URL)
        self.session = session

    def register_user(self, user_data, expected_status = 201):
        return self.send_requests(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )
    
    def login_user(self, login_data, expected_status = [200, 201]):
        return self.send_requests(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )
    
    def authenticate(self, user_creds):
        login_data = {
            "email": user_creds[0],
            "password": user_creds[1]
        }
        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")
        token = response["accessToken"]
        self._update_session_headers(**{"Authorization": f"Bearer {token}"})
