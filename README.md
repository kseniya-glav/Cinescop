## Установка
1. Клонирование репозитория
```git clone https://github.com/kseniya-glav/Cinescop.git```
2. Переход в директорию Cinescop
```cd Cinescope```
3. Создание виртуального окружения
```python3 -m venv venv```
4. Актировка виртуальной среды
```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process``` - изменение прав в текущем терминале (при необходимости)
```venv\Scripts\Activate```
5. Установка зависимостей
```pip3 install -r requirements.txt```  
    
## Запуск тестов
1. Запуск тестов  
1.1. Все тесты
```pytest```
1.2. С метками
```pytest -m slow``` - медленные тесты.
```pytest -m mock``` - тесты моковые данные.
```pytest -m authAPI``` - тесты регистрация и авторизация пользователя.
```pytest -m userAPI``` -  тесты crud-операции с пользователем.
```pytest -m moviesAPI``` - тесты crud-операции с фильмами.
```pytest -m transaction``` - тесты транзакция в бд.
2. Генерация отчёта allure
```allure serve ./allure-results```