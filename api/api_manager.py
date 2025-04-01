from api.auth_api import AuthAPI
from api.user_api import UserAPI
from api.movies_api import MoviesApi

class ApiManager:

    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.movies_api = MoviesApi(session)
        
    def close_session(self):
        self.session.close()
