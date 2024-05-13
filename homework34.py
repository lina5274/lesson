# Моделирование работы сети кафе с несколькими столиками и потоком посетителей, прибывающих для заказа пищи
# и уходящих после завершения приема.
#
# Есть сеть кафе с несколькими столиками. Посетители приходят, заказывают еду, занимают столик, употребляют еду и уходят.
# Если столик свободен, новый посетитель принимается к обслуживанию, иначе он становится в очередь на ожидание.
#
# Создайте 3 класса:
# Table - класс для столов, который будет содержать следующие атрибуты: number(int) - номер стола, is_busy(bool) - занят стол или нет.
#
# Cafe - класс для симуляции процессов в кафе. Должен содержать следующие атрибуты и методы:
# Атрибуты queue - очередь посетителей (создаётся внутри init), tables список столов (поступает из вне).
# Метод customer_arrival(self) - моделирует приход посетителя(каждую секунду).
# Метод serve_customer(self, customer) - моделирует обслуживание посетителя. Проверяет наличие свободных столов,
# в случае наличия стола - начинает обслуживание посетителя (запуск потока),
# в противном случае - посетитель поступает в очередь. Время обслуживания 5 секунд.
# Customer - класс (поток) посетителя. Запускается, если есть свободные столы.
#
# Так же должны выводиться текстовые сообщения соответствующие событиям:
# Посетитель номер <номер посетителя> прибыл.
# Посетитель номер <номер посетителя> сел за стол <номер стола>. (начало обслуживания)
# Посетитель номер <номер посетителя> покушал и ушёл. (конец обслуживания)
# Посетитель номер <номер посетителя> ожидает свободный стол. (помещение в очере
import threading
from threading import Thread
import time
import queue

class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

class Customer(Thread):
    def __init__(self, number, cafe):
        super().__init__()
        self.number = number
        self.cafe = cafe
        self.table = None

    def take_table(self, free_table):
        self.free_table = free_table
        free_table.is_busy = True

    def leave_table(self, free_table):
        self.table = None
        free_table.is_busy = False


    def run(self):
        self.cafe.serve_customer(customer)


class Cafe:
    def __init__(self, tables):
        self.q = queue.Queue()
        self.tables = tables
        self.locker = threading.Lock()

    def check_table(self):
        for table in self.tables:
            if not table.is_busy:
                return table
        return False

    def customer_arrival(self, customer):
       for customer_number in range(1, 21):
           customer = Customer(customer_number, self)
           with self.locker:
                print(f'Посетитель номер {customer_number} прибыл')
                if not self.check_table():
                    print(f'Посетитель номер {customer_number} ожидает свободный стол')
                    time.sleep(1)
           customer.start()
           self.q.put(customer)



    def serve_customer(self, customer):
        free_table = self.check_table()
        while not self.q.empty() and free_table:
            cur_customer = self.q.get()
            with self.locker:
                print(f'Посетитель номер {customer_number} сел за стол {table_number}')
                cur_customer.take_table(free_table)
                time.sleep(1)
            time.sleep(4)
            with self.locker:
                print(f'Посетитель номер {customer_number} покушал и ушёл.')
                cur_customer.leave_table(free_table)
                time.sleep(1)
                free_table = self.check_table


table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]
cafe = Cafe(tables)
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()
customer_arrival_thread.join()







