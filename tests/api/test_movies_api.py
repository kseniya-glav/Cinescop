import pytest
import random
from constants.roles import Roles

class TestMoviesAPI:
    
    def test_get_all_movies(self, common_user):
        """Получение списка всех фильмов"""
        data = common_user.api.movies_api.get_movies().json()
        assert data["pageSize"] == len(data["movies"]), "Списка фильмов нет"

    @pytest.mark.parametrize("maxPrice,locations,genreId", [(1000, "MSK", 1), (1000, "SPB", 1)])
    def test_get_filter_movies(self, common_user, maxPrice, locations, genreId):
        """Получение списка фильмов с фильтрацией по `locations`"""
        json_filter = {
            "maxPrice": maxPrice,
            "locations": locations,
            "genreId": genreId
            }
        data = common_user.api.movies_api.get_movies(params = json_filter).json()
        assert len([movie["location"] for movie in data["movies"] if 
                    movie["location"]==locations and movie["genreId"]==genreId 
                    and movie["price"] > 0 and movie["price"] < maxPrice]) == len(data["movies"])

    def test_failed_get_movies(self, common_user):
        """Передача неверных параметров"""
        json_filter = {
            "minPrice" : "-1000"
            }
        response = common_user.api.movies_api.get_movies(expected_status = 400, params = json_filter)
        assert "error" in response.json(), "Ошибки нет"

    def test_post_movies_valid_data(self, super_admin, new_movies):
        """Создание фильма с валидными данными (**SUPER_ADMIN**)"""
        response = super_admin.api.movies_api.post_movies(json = new_movies)
        id_create_movie = response.json()["id"]
        response = super_admin.api.movies_api.get_movies_id(id_create_movie)
        assert response.json()["id"] == id_create_movie, "Фильма нет в списке"

    def test_post_movies_min_valid_data(self, super_admin, new_movies_min):
        """Создание фильма с валидными данными (**SUPER_ADMIN**)"""
        response = super_admin.api.movies_api.post_movies(json = new_movies_min)
        id_create_movie = response.json()["id"]
        response = super_admin.api.movies_api.get_movies_id(id_create_movie)
        assert response.json()["id"] == id_create_movie, "Фильма нет в списке"

    def test_failed_post_movies(self, super_admin, new_movies):
        """Создание фильма с уже существующим названием."""
        response = super_admin.api.movies_api.get_movies()
        new_movies["name"] = response.json()["movies"][0]["name"]
        response = super_admin.api.movies_api.post_movies(json = new_movies, expected_status = 409)
        assert "error" in response.json(), "Ошибки нет"

    def test_get_movies_id(self, common_user):
        """Получение фильма по валидному ID."""
        response = common_user.api.movies_api.get_movies()
        movie_id = [movie["id"] for movie in response.json()["movies"]][0]
        response = common_user.api.movies_api.get_movies_id(movie_id)
        assert response.json()["id"] == movie_id, "Фильм не тот"

    def test_failed_get_movies_id(self, common_user):
        """Получение фильма с несуществующим ID."""
        response = common_user.api.movies_api.get_movies()
        not_movie_id = max([movie["id"] for movie in response.json()["movies"]]) + 1000
        response = common_user.api.movies_api.get_movies_id(not_movie_id, expected_status = 404)
        assert "error" in response.json(), "Ошибки нет"

    @pytest.mark.parametrize("user_with_roles,expected_status", [([Roles.USER], 403), ([Roles.ADMIN], 403), ([Roles.SUPER_ADMIN], 200)], indirect=["user_with_roles"])
    def test_delete_movies_id(self, create_movies, user_with_roles, expected_status):
        """Удаление фильма, с правом доступа и без права доступа."""
        movie_id = create_movies["id"]
        response = user_with_roles.api.movies_api.delete_movies(movie_id, expected_status = expected_status)
        assert "error" not in response.json() if expected_status == 200 else "error" in response.json()


    def test_failed_delete_movies_id(self, super_admin):
        """Удаление несуществующего фильма."""
        response = super_admin.api.movies_api.get_movies()
        not_movie_id = max([movie["id"] for movie in response.json()["movies"]]) + 1000
        response = super_admin.api.movies_api.delete_movies(not_movie_id, expected_status = 404)
        assert "error" in response.json(), "Ошибки нет"
        
    def test_get_movies_reviews_id(self, common_user):
        """Получение всех отзывов для фильма."""
        response = common_user.api.movies_api.get_movies()
        movie_id = random.choice([movie["id"] for movie in response.json()["movies"]])
        data = common_user.api.movies_api.get_movies_reviews_id(movie_id).json()
        assert data[0]["user"]["fullName"] if data else type(data) == list, "Список отзывов отсутствует"

    def test_failed_role(self, common_user, new_movies):
        """Создание фильма, без права доступа."""   
        response = common_user.api.movies_api.post_movies(json = new_movies, expected_status = 403)
        assert "error" in response.json(), "Ошибки нет"