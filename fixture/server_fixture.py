import subprocess
import time
import pytest
import requests

# Фикстура для запуска сервера
@pytest.fixture(scope="session")
def server_worldclockapi():
    server_process = subprocess.Popen(["python", "test_services/service_fake_worldclockapi.py"])
    time.sleep(5)
    yield server_process
    server_process.terminate()
    server_process.wait()
       
       
@pytest.fixture(scope="session")
def server_what_is_today():
    server_process = subprocess.Popen(["python", "test_services\service_what_is_today.py"])
    time.sleep(5)
    yield server_process 
    server_process.terminate()
    server_process.wait()


@pytest.fixture(scope="session")
def wiremock_container():
    """
    Фикстура для запуска контейнера WireMock.
    Контейнер запускается перед всеми тестами и останавливается после их завершения.
    """
    try:
        subprocess.run(
            ["docker", "run", "-d", "--rm", "-p", "8080:8080", "--name", "wiremock", "wiremock/wiremock:3.12.0"],
            check=True
        )
        time.sleep(5)
        yield  # Передача контроля тестам
    finally:
        subprocess.run(["docker", "stop", "wiremock"], check=False)


@pytest.fixture(scope="session")
def run_wiremock_worldclockap_time(wiremock_container):
    """Запуск и настройка WireMock сервера"""
    wiremock_url = "http://localhost:8080/__admin/mappings"
    mapping = {
        "request": {
            "method": "GET",
            "url": "/wire/mock/api/json/utc/now"  # Эмулируем запрос к worldclockapi
        },
        "response": {
            "status": 200,
            "body": '''{
                "$id": "1",
                "currentDateTime": "2025-03-08T00:00Z",
                "utcOffset": "00:00",
                "isDayLightSavingsTime": false,
                "dayOfTheWeek": "Wednesday",
                "timeZoneName": "UTC",
                "currentFileTime": 1324567890123,
                "ordinalDate": "2025-1",
                "serviceResponse": null
            }'''
        }
    }
    response = requests.post(wiremock_url, json=mapping)
    assert response.status_code == 201, "Не удалось настроить WireMock"
    