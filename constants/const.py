API_DEV_CINESCOPE_URL = "https://api.dev-cinescope.coconutqa.ru"
AUTH_DEV_CINESCOPE_URL = "https://auth.dev-cinescope.coconutqa.ru"
DEV_CINESCOPE_URL = "https://dev-cinescope.coconutqa.ru"

BASE_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

MOVIES_ENDPOINT = "/movies"
MOVIES_ID_ENDPOINT = "/movies/{id}"
MOVIES_ID_REVIEWS_ENDPOINT = "/movies/{id}/reviews"
GENRES_ENDPOINT = "/genres"
GENRES_ID_ENDPOINT = "/genres/{id}"

REGISTER_ENDPOINT = "/register"
LOGIN_ENDPOINT = "/login"

USER_ENDPOINT = "/user"
USER_LOCATOR_ENDPOINT = "/user/{user_locator}"

GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'
BLUE = '\033[34m'