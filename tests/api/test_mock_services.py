import requests
from pydantic import BaseModel, Field
from pytest_mock import mocker
from unittest.mock import Mock
from datetime import datetime
import pytz
import pytest
import allure


# Модель Pydantic для ответа сервера worldclockapi
class WorldClockResponse(BaseModel):
    id: str = Field(alias="$id")  # Используем алиас для поля "$id"
    currentDateTime: str
    utcOffset: str
    isDayLightSavingsTime: bool
    dayOfTheWeek: str
    timeZoneName: str
    currentFileTime: int
    ordinalDate: str
    serviceResponse: None

    class Config:
        # Разрешаем использование алиасов при парсинге JSON
        validate_by_name = True


# Модель для запроса к сервису TodayIsHoliday
class DateTimeRequest(BaseModel):
    currentDateTime: str  # Формат: "2025-02-13T21:43Z"

# Модель для ответа от сервиса TodayIsHoliday
class WhatIsTodayResponse(BaseModel):
    message: str

#Функция выолняющая запрос в сервис worldclockapi для получения текущей даты
def get_worldclockap_time() -> WorldClockResponse:
    # Выполняем GET-запрос
    response = requests.get("http://worldclockapi.com/api/json/utc/now") #Запрос в реальный сервис
    # Проверяем статус ответа
    assert response.status_code == 200, "Удаленный сервис недоступен"
    # Парсим JSON-ответ с использованием Pydantic модели
    return  WorldClockResponse(**response.json())
    #Modul_4\Cinescope\tests\api\test_mock_services.py
    #Функция выполняющая запрос в Fake сервис worldclockapi для получения текущей даты 
    
def get_fake_worldclockap_time() -> WorldClockResponse:
        # Выполняем GET-запрос
    response = requests.get("http://127.0.0.1:16001/fake/worldclockapi/api/json/utc/now")  #Запрос в фейк сервис
        # Проверяем статус ответа
    assert response.status_code == 200, "Удаленный сервис недоступен"
        # Парсим JSON-ответ с использованием Pydantic модели
    return  WorldClockResponse(**response.json())

@allure.epic("Тестирование сервиса TodayIsHoliday")
@allure.feature("Тестирование работоспособности сервисов worldclockap")
@pytest.mark.mock
class TestTodayIsHolidayServiceAPI:
    """
    Нужно протестировать сервис (“TodayIsHoliday"), оговорено что он должен брать данные из другого сервиса и возвращать результат.
    какие минусы в этом подходе?
        - необходим доступ в интернет
        - тест нестабилен. он проверяет что сегодня нет праздника однако если запустить его скажем 1 января данный тест не пройдет
        - время прохождения теста увеличено из-за дополнительного запроса в сторонний сервис
        - сторонний сервис может быть недоступен (из-за не уплаты. DDOS атаки и иных причин )
        - тест должен проверять то что необходимо и не должен содержать излишних зависимостей
    """
    @pytest.mark.slow
    def test_worldclockap(self):# проверка работоспособности сервиса worldclockap
        world_clock_response = get_worldclockap_time()
        # Выводим текущую дату и время
        current_date_time = world_clock_response.currentDateTime
        assert current_date_time == datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%MZ"), "Дата не совпадает"

    @pytest.mark.slow
    @pytest.mark.usefixtures("server_what_is_today")
    def test_what_is_today(self):# проверка работоспособности Fake сервиса what_is_today
        # Запрашиваем текущее время у сервиса worldclockap
        world_clock_response = get_worldclockap_time()
        what_is_today_response = requests.post("http://127.0.0.1:16002/what_is_today", 
                                               data=DateTimeRequest(currentDateTime=world_clock_response.currentDateTime).model_dump_json()
                                               )
        # Проверяем статус ответа от тестируемогосервиса
        assert what_is_today_response.status_code == 200, "Удаленный сервис недоступен"
        # Парсим JSON-ответ от тестируемого сервиса с использованием Pydantic модели
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
        #Проводим валидацию ответа тестируемого сервиса
        assert what_is_today_data.message ==  "Сегодня нет праздников в России.", "Сегодня нет праздника!"

@allure.epic("Тестирование сервиса TodayIsHoliday")
@allure.feature("Тестирование Mock")
@pytest.mark.mock
class TestByMockTodayIsHolidayServiceAPI:
    """
    Используйте моки, когда нужно проверить взаимодействие с зависимостями.
    """
    @pytest.mark.usefixtures("server_what_is_today")
    def test_what_is_today_BY_MOCK(self, mocker):
        # Создаем мок для функции get_worldclockap_time
        mocker.patch(
            "test_mock_services.get_worldclockap_time",  # Указываем путь к функции в нашем модуле (формат файл.класс.метод)
                                               # либо имя_файла.имя_метода если он находится  вэтом же файле
            return_value=Mock(
                currentDateTime="2025-01-01T00:00Z"  # Фиксированная дата для возврата из мок функции "1 января"
            )
        )
        # Выполним тело предыдущего теста еще раз
        world_clock_response = get_worldclockap_time() # = "2025-01-01T00:00Z"
        what_is_today_response = requests.post("http://127.0.0.1:16002/what_is_today", 
                                               data=DateTimeRequest(currentDateTime=world_clock_response.currentDateTime).model_dump_json()
                                               )
        # Проверяем статус ответа от тестируемого сервиса
        assert what_is_today_response.status_code == 200, "Удаленный сервис недоступен"
        # Парсим JSON-ответ от тестируемого сервиса с использованием Pydantic модели
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
        assert what_is_today_data.message == "Новый год", "ДОЛЖЕН БЫТЬ НОВЫЙ ГОД!"

@allure.epic("Тестирование сервиса TodayIsHoliday")
@allure.feature("Тестирование Stub")
@pytest.mark.mock
class TestStubTodayIsHolidayServiceAPI:
    """
    Используйте стабы, когда нужно имитировать определённые ответы.
    """
    def stub_get_worldclockap_time(self):
        class StubWorldClockResponse:
            def __init__(self):
                self.currentDateTime = "2025-05-09T00:00Z"  # Фиксированная дата для Stub
        return StubWorldClockResponse()

    @pytest.mark.usefixtures("server_what_is_today")
    def test_what_is_today_BY_STUB(self, monkeypatch):
        # Подменяем реальную функцию get_worldclockap_time на Stub
        monkeypatch.setattr("test_mock_services.get_worldclockap_time", self.stub_get_worldclockap_time)
        #или же можем просто напрямую взять значение из Stub world_clock_response = stub_get_worldclockap_time()
        # Выполним тело предыдущего теста еще раз
        world_clock_response = get_worldclockap_time()  # Произойдет вызов Stub, возвращающего "2025-01-01T00:00Z"
        # Выполняем запрос к тестируемому сервису
        what_is_today_response = requests.post(
            "http://127.0.0.1:16002/what_is_today",
            data=DateTimeRequest(currentDateTime=world_clock_response.currentDateTime).model_dump_json()
        )
        # Проверяем статус ответа от тестируемого сервиса
        assert what_is_today_response.status_code == 200, "Удаленный сервис недоступен"
        # Парсим JSON-ответ от тестируемого сервиса с использованием Pydantic модели
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
        # Проверяем, что ответ соответствует ожидаемому
        assert what_is_today_data.message == "День Победы", "ДОЛЖЕН БЫТЬ ДЕНЬ ПОБЕДЫ!"

@allure.epic("Тестирование сервиса TodayIsHoliday")
@allure.feature("Тестирование WireMock")
@pytest.mark.mock
class TestWireMockTodayIsHolidayServiceAPI:
    """
    Используйте WireMock, когда нужно эмулировать HTTP-API для интеграционного тестирования.
    """
    @pytest.mark.slow
    @pytest.mark.usefixtures("server_what_is_today", "run_wiremock_worldclockap_time")
    def test_what_is_today_BY_WIREMOCK(self): #Данный тест максимально похож на базовый 
        # Выполняем запрос к WireMock (имитация worldclockapi)
        world_clock_response = requests.get("http://localhost:8080/wire/mock/api/json/utc/now")
        assert world_clock_response.status_code == 200, "Удаленный сервис недоступен"
        # Парсим JSON-ответ с использованием Pydantic модели
        current_date_time = WorldClockResponse(**world_clock_response.json()).currentDateTime

        # Выполняем запрос к тестируемому сервису what_is_today
        what_is_today_response = requests.post(
            "http://127.0.0.1:16002/what_is_today",
            data=DateTimeRequest(currentDateTime=current_date_time).model_dump_json()
        )

        # Проверяем статус ответа от тестируемого сервиса
        assert what_is_today_response.status_code == 200, "Удаленный сервис недоступен"
        # Парсим JSON-ответ от тестируемого сервиса с использованием Pydantic модели
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
        # Проверяем, что ответ соответствует ожидаемому
        assert what_is_today_data.message == "Международный женский день", "8 марта же?"

@allure.epic("Тестирование сервиса TodayIsHoliday")
@allure.feature("Тестирование Fake")
@pytest.mark.mock
class TestFakeTodayIsHolidayServiceAPI:
    """
    Используйте Fake сервисы, когда нужна упрощённая реализация реального сервиса.
    """
    @pytest.mark.slow
    @pytest.mark.usefixtures("server_worldclockapi")
    def test_fake_worldclockap(self):# проверка работоспособности сервиса worldclockap
        world_clock_response = get_fake_worldclockap_time()
        # Выводим текущую дату и время
        current_date_time = world_clock_response.currentDateTime
        print(f"Текущая дата и время: {current_date_time=}")
 
        assert current_date_time == datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%MZ"), "Дата не совпадает"
    
    @pytest.mark.slow
    @pytest.mark.usefixtures("server_what_is_today", "server_worldclockapi")
    def test_fake_what_is_today(self):# проверка работоспособности Fake сервиса what_is_today
        world_clock_response = get_fake_worldclockap_time()
        what_is_today_response = requests.post("http://127.0.0.1:16002/what_is_today", 
                                               data=DateTimeRequest(currentDateTime=world_clock_response.currentDateTime).model_dump_json()
                                               )
        # Проверяем статус ответа от тестируемого сервиса
        assert what_is_today_response.status_code == 200, "Удаленный сервис недоступен"
        # Парсим JSON-ответ от тестируемого сервиса с использованием Pydantic модели
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
        assert what_is_today_data.message ==  "Сегодня нет праздников в России.", "Сегодня нет праздника!"