from models.db_model import AccountTransactionTemplate
from utils.data_generator import DataGenerator
import pytest
import random
import allure

@allure.epic("Тестирование транзакций")
@allure.feature("Тестирование транзакций между счетами")
@pytest.mark.transaction
class TestAccountTransactionTemplate:

    @allure.story("Корректность перевода денег между двумя счетами")
    @allure.description("""
    Этот тест проверяет корректность перевода денег между двумя счетами.
    Шаги:
    1. Создание двух счетов: Stan и Bob.
    2. Перевод 200 единиц от Stan к Bob.
    3. Проверка изменения балансов.
    4. Очистка тестовых данных.
    """)
    @allure.title("Тест перевода денег между счетами 200 рублей")
    def test_accounts_transaction_template(self, db_session):

        with allure.step("Создание тестовых данных в базе данных: счета Stan и Bob"):
            stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_int(10)}", balance=random.randint(500, 2000))
            bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_int(10)}", balance=random.randint(1000, 3000))
            db_session.add_all([stan, bob])
            db_session.commit()
        
        @allure.step("Функция перевода денег: transfer_money")
        @allure.description( """
            функция выполняющая транзакцию, имитация вызова функции на стороне тестируемого сервиса
            и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
            """)
        def transfer_money(session, from_account, to_account, amount): 
            with allure.step(" Получаем счета"):
                from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
                to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()    
            with allure.step("Проверяем, что на счете достаточно средств"):
                if from_account.balance < amount:
                    raise ValueError("Недостаточно средств на счете")
            with allure.step("Выполняем перевод"):
                from_account.balance -= amount
                to_account.balance += amount
            with allure.step("Сохраняем изменения"):
                session.commit()

        # ===== Тест ===== 
        with allure.step("Запоминаем начальные балансы"):
            start_balance_stan = stan.balance
            start_balance_bob = bob.balance

        try:
            with allure.step("Генерируем сумма перевода (у.е.) от stan к bob и выполняем перевод"):
                amount = random.randint(500, 1500)
                transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=amount)
            with allure.step("Проверяем, что балансы изменились"):
                assert stan.balance == start_balance_stan - amount
                assert bob.balance == start_balance_bob + amount

        except Exception as e:
            with allure.step("ОШИБКА откаты транзакции"):
                db_session.rollback()
            with allure.step("Проверяем, что балансы после отката вернулись в начальные"):
                stan = db_session.query(AccountTransactionTemplate).filter_by(user=stan.user).one()
                bob = db_session.query(AccountTransactionTemplate).filter_by(user=bob.user).one()
                assert stan.balance == start_balance_stan
                assert bob.balance == start_balance_bob
              
        finally:
            with allure.step("Удаляем данные для тестирования из базы"):
                db_session.delete(stan)
                db_session.delete(bob)
                db_session.commit()
                