from threading import Thread, Lock
import random
import time

class Bank(Thread):
    def __init__(self):
        super().__init__()
        self.balance = 0
        self.lock = Lock()

    def deposit(self):
        for i in range(100):
            if self.balance >= 500 and self.lock.locked():
                 self.lock.release()
            first = random.randint(50, 500)
            self.balance += first
            print(f'Пополнение: {first}. Баланс: {self.balance}')
            time.sleep(0.001)

    def take(self):
        for i in range(100):
            second = random.randint(50,500)
            print(f'Запрос на {second}')
            if self.balance >= second:
                self.balance -= second
                print(f'Снятие: {second}. Баланс: {self.balance}')
            else:
                print(f'Запрос отклонён, недостаточно средств')
                self.lock.acquire()
            time.sleep(0.001)


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = Thread(target=Bank.deposit, args=(bk,))
th2 = Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
