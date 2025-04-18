import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resources.db_creds import DataBaseMoviesCreds as db
from models.db_model import UserDBModel
from utils.data_generator import DataGenerator
import datetime
engine = create_engine(f"postgresql+psycopg2://{db.USERNAME}:{db.PASSWORD}@{db.HOST}:{db.PORT}/{db.NAME}") # Создаем движок (engine) для подключения к базе данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Создаем фабрику сессий

@pytest.fixture(scope="module")
def db_session():
    """
    Фикстура с областью видимости module.
    Тестовые данные создаются один раз для всех тестов в модуле.
    """
    session = SessionLocal()
    
    test_user = UserDBModel(
        id = "test_id2",
        email = DataGenerator.generate_random_email(),
        full_name = DataGenerator.generate_random_name(),
        password = DataGenerator.generate_random_password(),
        created_at = datetime.datetime.now(),
        updated_at = datetime.datetime.now(),
        verified = False,
        banned = False,
        roles = "{USER}"
    )
    
    session.add(test_user) #добавляем обьект в базу данных
    session.commit() #сохраняем изменения для всех остальных подключений
    
    yield session
    
    session.delete(test_user)
    session.commit()
    session.close()
    