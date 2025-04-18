import random
import string
from faker import Faker

faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 10))
        return f"kek{random_string}@gmail.com"
    
    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"
    
    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)

        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = ''.join(random.choices(all_chars, k = remaining_length))

        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)
    
    @staticmethod
    def valid_data_for_create_movies():
        return {
            "name": faker.catch_phrase(),
            "imageUrl": faker.image_url(),
            "price": random.randint(100, 1000),
            "description": faker.text(max_nb_chars=250),
            "location": random.choice(["SPB", "MSK"]),
            "published": random.choice([True, False]),
            "genreId": random.randint(1, 10)
        }
                
    @staticmethod
    def min_valid_data_for_create_movies():
        return {
            "name": faker.catch_phrase(),
            "price": random.randint(100, 1000),
            "description": faker.text(max_nb_chars=250),
            "location": random.choice(["SPB", "MSK"]),
            "published": random.choice([True, False]),
            "genreId": random.randint(1, 10)
        }
          
    def generate_random_int(length):
        return ''.join(str(random.randint(0,9)) for _ in range(length))
    