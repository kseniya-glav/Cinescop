import pytest
import random
from constants.roles import Roles
from pytz import timezone
from models.db_model import MovieDBModel
from models.movies_model import AllMovies, MovieSchema, MovieGetId, Review
from models.other_model import ErrorResponse
import datetime
import allure

@allure.epic("Тестирование сущности фильм")
@allure.feature("Тестирование crud-операций")
@pytest.mark.moviesAPI
class TestMoviesAPI:
    
    @allure.title("Получение списка всех фильмов")
    def test_get_all_movies(self, common_user):
        with allure.step("Получаем список фильмов"):
            data = AllMovies(**common_user.api.movies_api.get_movies().json())
        with allure.step("Проверяем количество объектов с фильмами и указанное количество фильмов в ответе"):
            assert data.pageSize == len(data.movies), "Списка фильмов нет"

    @allure.title("Получение списка фильмов с фильтрацией")
    @pytest.mark.parametrize("maxPrice,locations,genreId", [(1000, "MSK", 1), (1000, "SPB", 1)])
    def test_get_filter_movies(self, common_user, maxPrice, locations, genreId):
        with allure.step("Инициализируем тестовые данные"):
            json_filter = {
                "maxPrice": maxPrice,
                "locations": locations,
                "genreId": genreId
                }
        with allure.step("Получаем список фильмов с учётом параметров"):
            data = AllMovies(**common_user.api.movies_api.get_movies(params = json_filter).json())
        with allure.step("Проверяем количество объектов с фильмами по заданным параметрам и указанное количество фильмов в ответе"):
            assert len([movie.location for movie in data.movies if 
                movie.location == locations and movie.genreId == genreId and movie.price < maxPrice]) == len(data.movies)

    @allure.title("Передача неверных параметров")
    def test_failed_get_movies(self, common_user):
        with allure.step("Инициализируем тестовые данные"):
            json_filter = {
                "minPrice" : "-1000"
            }
        with allure.step("ОШИБКА: передан неверный параметр"):
            assert ErrorResponse(**common_user.api.movies_api.get_movies(expected_status = 400, params = json_filter).json())

    @allure.title("Создание фильма с валидными данными")
    def test_post_movies_valid_data(self, super_admin, new_movies):
        with allure.step("Создаём новый фильм"):
            response = MovieSchema(**super_admin.api.movies_api.post_movies(json = new_movies).json())
            id_create_movie = response.id
        with allure.step("Получаем новый фильм"):
            response = MovieGetId(**super_admin.api.movies_api.get_movies_id(id_create_movie).json())
        with allure.step("Проверяем id нового фильма и id фильма из ответа"):
            assert response.id == id_create_movie, "Фильма нет в списке"

    @allure.title("Создание фильма с минимальными валидными данными")
    def test_post_movies_min_valid_data(self, super_admin, new_movies_min):
        with allure.step("Создаём новый фильм"):
            response = MovieSchema(**super_admin.api.movies_api.post_movies(json = new_movies_min).json())
            id_create_movie = response.id
        with allure.step("Получаем новый фильм"):
            response = MovieGetId(**super_admin.api.movies_api.get_movies_id(id_create_movie).json())
        with allure.step("Проверяем id нового фильма и id фильма из ответа"):
            assert response.id == id_create_movie, "Фильма нет в списке"
    
    @allure.title("Создание фильма с уже существующим названием.")
    def test_failed_post_movies(self, super_admin, new_movies):
        with allure.step("Получаем список фильмов"):
            response = AllMovies(**super_admin.api.movies_api.get_movies().json())
        with allure.step("В тестовых данных в поле название фильма прописываем уже существующее имя"):
            new_movies["name"] = response.movies[0].name
        with allure.step("ОШИБКА: фильм с таким названием уже существует"):
            assert ErrorResponse(**super_admin.api.movies_api.post_movies(json = new_movies, expected_status = 409).json()), "Ошибки нет"

    @allure.title("Получение фильма по валидному ID.")
    def test_get_movies_id(self, common_user):
        with allure.step("Получаем список фильмов и берём id первого фильма"):
            response = AllMovies(**common_user.api.movies_api.get_movies().json())
            movie_id = [movie.id for movie in response.movies][0]
        with allure.step("Получаем фильм по взятому id"):
            response = MovieGetId(**common_user.api.movies_api.get_movies_id(movie_id).json())
        with allure.step("Проверяем корректность полученного id"):
            assert response.id == movie_id, "Фильм не тот"

    @allure.title("Получение фильма с несуществующим ID.")
    def test_failed_get_movies_id(self, common_user):
        with allure.step("Получаем список фильмов"):
            response = AllMovies(**common_user.api.movies_api.get_movies().json())
        with allure.step("Создаём несуществующий id"):
            not_movie_id = max([movie.id for movie in response.movies]) + 1000
        with allure.step("ОШИБКА: нет фильма с таким id"):
            assert ErrorResponse(**common_user.api.movies_api.get_movies_id(not_movie_id, expected_status = 404).json())

    @allure.title("Удаление фильма, с правом доступа и без права доступа.")
    @pytest.mark.parametrize("user_with_roles,expected_status", [([Roles.USER], 403), ([Roles.ADMIN], 403), ([Roles.SUPER_ADMIN], 200)], indirect=["user_with_roles"])
    def test_delete_movies_id(self, create_movies, user_with_roles, expected_status):
        with allure.step("Получаем id из созданного фильма"):
            movie_id = create_movies.id
        with allure.step("Отправляем запрос на удаление фильма"):
            response = user_with_roles.api.movies_api.delete_movies(movie_id, expected_status = expected_status)
        if expected_status == 200:
            with allure.step("Запрос прошёл успешно"):
                assert MovieSchema(**response.json())
        else:   
            with allure.step("ОШИБКА: нет права на удаление"):
                assert ErrorResponse(**response.json())

    @allure.title("Удаление несуществующего фильма.")
    def test_failed_delete_movies_id(self, super_admin):
        with allure.step("Получаем список фильмов"):
            response =  AllMovies(**super_admin.api.movies_api.get_movies().json())
        with allure.step("Создаём несуществующий id"):
            not_movie_id = max([movie.id for movie in response.movies]) + 1000
        with allure.step("ОШИБКА: невозможно удалить фильм с несуществующим id"):
            assert ErrorResponse(**super_admin.api.movies_api.delete_movies(not_movie_id, expected_status = 404).json())
        
    @allure.title("Получение всех отзывов для фильма.")
    def test_get_movies_reviews_id(self, common_user):
        with allure.step("Получаем список фильмов"):
            response =  AllMovies(**common_user.api.movies_api.get_movies().json())
        with allure.step("Выбираем случайный фильм"):
            movie_id = random.choice([movie.id for movie in response.movies])
        with allure.step("Получаем отзывы по выбранному фильму"):
            data = [Review(**item) for item in common_user.api.movies_api.get_movies_reviews_id(movie_id).json()]
        with allure.step("Проверяем наличие имени комментатора или пустой список"):
            assert data[0].user.fullName if data else type(data) == list

    @allure.title("Создание фильма, без права доступа.")
    def test_failed_role(self, common_user, new_movies):
        with allure.step("ОШИБКА: нет доступа для создания фильма"):
            assert ErrorResponse(**common_user.api.movies_api.post_movies(json = new_movies, expected_status = 403).json())
        
    @allure.title("Создание и удаление фильма с проверкой в базе данных")
    def test_create_delete_movie(self, new_movies, super_admin, db_session):
        with allure.step("Проверяем отсутствие фильма с названием, идентичным новому"):
            assert not db_session.query(MovieDBModel).filter(MovieDBModel.name == new_movies["name"]).count(), "В базе уже присутствует фильм с таким названием"
        with allure.step("Добавляем новый фильм"):
            response = MovieSchema(**super_admin.api.movies_api.post_movies(json = new_movies).json())
        with allure.step("Проверяем наличие фильма с названием, идентичным новому"):
            movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == new_movies["name"])
            assert (movies_from_db).count(), "В базе уже присутствует фильм с таким названием"
            assert movies_from_db.first().created_at >= (datetime.datetime.now(timezone('UTC')).replace(tzinfo=None) - datetime.timedelta(minutes=5)), "Сервис выставил время создания с большой погрешностью"
        with allure.step("Удаляем добавленный фильм"):
            assert MovieSchema(**super_admin.api.movies_api.delete_movies(id=response.id).json())
        with allure.step("Проверяем отсутствие удаленного фильма в базе"):
            assert not db_session.query(MovieDBModel).filter(MovieDBModel.name == new_movies["name"]).count(), "Фильм не был удален из базы!"
