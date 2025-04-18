from custom_requester.custom_requester import CustomRequester
from constants.const import AUTH_DEV_CINESCOPE_URL, USER_ENDPOINT, USER_LOCATOR_ENDPOINT

class UserAPI(CustomRequester):
    """Класс для работы с API пользователей."""
    def __init__(self, session):
        super().__init__(session= session, base_url = AUTH_DEV_CINESCOPE_URL)
        self.session = session

    def get_user(self, user_locator, expected_status = 200):
        return self.send_requests(
            method = "GET",
            endpoint = USER_LOCATOR_ENDPOINT.format(user_locator = user_locator),
            expected_status = expected_status
        )
        
    def create_user(self, user_data, expected_statuc = 201):
        return self.send_requests(
            method="POST",
            endpoint=USER_ENDPOINT,
            data = user_data,
            expected_status=expected_statuc
        )

    '''def get_user_info(self, user_id, expected_status = 200):
        return self.send_request(
            method = "GET",
            endpoint = f"/users/{user_id}",
            expected_status = expected_status
        )
    
    
    def delete_user(self, user_id, expected_status=204):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )'''

    
