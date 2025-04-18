from faker import Faker
import pytest
import requests
from constants.const import API_DEV_CINESCOPE_URL
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
from entities.user import User
from resources.user_creds import SuperAdminCreds
from constants.roles import Roles
from models.user_model import UserRegistr, UserRegistrResponse
from models.movies_model import MovieSchema

faker = Faker()

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    http_session.base_url = API_DEV_CINESCOPE_URL
    yield http_session
    http_session.close()
    
    
@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture
def new_movies():
    return DataGenerator.valid_data_for_create_movies()


@pytest.fixture
def new_movies_min():
    return DataGenerator.min_valid_data_for_create_movies()


@pytest.fixture(scope="session")
def admin(api_manager):
    api_manager.auth_api.authenticate({"email": SuperAdminCreds.USERNAME, "password": SuperAdminCreds.PASSWORD})
    return api_manager


@pytest.fixture
def create_movies(super_admin, new_movies):
    return MovieSchema(**super_admin.api.movies_api.post_movies(json = new_movies).json())


@pytest.fixture
def test_user() -> UserRegistr:
    """Генерация случайного пользователя для тестов."""
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()
    return UserRegistr(
        email =  random_email,
        fullName =  random_name,
        password =  random_password,
        passwordRepeat = random_password,
        roles = [Roles.USER.value]
    )


@pytest.fixture
def registered_user(api_manager, test_user) -> UserRegistr:
    """Фикстура для регистрации и получения данных зарегистрированного пользователя."""
    response = api_manager.auth_api.register_user(test_user, expected_status = [201, 409])
    assert UserRegistrResponse(**response.json()).email == test_user.email, "Email не совпадает"
    return test_user


@pytest.fixture(scope="session")
def requester():
    """Фикстура для создания экземпляра CustomRequester."""
    return CustomRequester(base_url=API_DEV_CINESCOPE_URL)


@pytest.fixture
def user_session():
    user_pool = []
    
    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session
    
    yield _create_user_session
    
    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()
    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )
    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="function")
def creation_user_data(test_user) -> UserRegistr:
    updated_data = test_user
    updated_data.verified = True
    updated_data.banned = False
    return UserRegistr(
        email =  updated_data.email,
        fullName =  updated_data.fullName,
        password =  updated_data.password,
        passwordRepeat = updated_data.passwordRepeat,
        roles = updated_data.roles,
        verified = updated_data.verified,
        banned = updated_data.banned
    )


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()
    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def common_admin(user_session, super_admin, creation_user_data):
    new_session = user_session()
    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def user_with_roles(request, user_session, super_admin, creation_user_data):
    new_session = user_session()
    roles = request.param
    if Roles.SUPER_ADMIN in roles:
        return super_admin
    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        roles,
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def registration_user_data() -> UserRegistr:
    random_password = DataGenerator.generate_random_password()
    return UserRegistr(
        email = DataGenerator.generate_random_email(),
        fullName = DataGenerator.generate_random_name(),
        password = random_password,
        passwordRepeat = random_password,
        roles = [Roles.USER.value]
    )
