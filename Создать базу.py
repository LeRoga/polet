from tkinter import *
from tkinter import ttk
import sqlite3

connection = sqlite3.connect('polet.db')
cursor = connection.cursor()

# Dropping existing tables
cursor.execute('DROP TABLE IF EXISTS tickets')
cursor.execute('DROP TABLE IF EXISTS clients')
cursor.execute('DROP TABLE IF EXISTS planes')
cursor.execute('DROP TABLE IF EXISTS airports')

# Creating planes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS planes (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    model TEXT NOT NULL,
    max_cargo INTEGER NOT NULL
)
''')

# Creating airports table
cursor.execute('''
CREATE TABLE IF NOT EXISTS airports (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL
)
''')

# Creating tickets table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    route TEXT NOT NULL,
    point TEXT NOT NULL,
    id_i INTEGER,
    id_p INTEGER,
    flight_date TEXT NOT NULL,
    duration INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (id_i) REFERENCES airports(id) ON DELETE CASCADE,
    FOREIGN KEY (id_p) REFERENCES planes(id) ON DELETE CASCADE
)
''')

# Creating clients table
cursor.execute('''
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    id_a INTEGER,
    Lname TEXT NOT NULL,
    Fname TEXT NOT NULL,
    patronymic TEXT,
    adress TEXT NOT NULL,
    city TEXT NOT NULL,
    discount REAL,
    order_date TEXT NOT NULL,
    FOREIGN KEY (id_a) REFERENCES tickets(id) ON DELETE CASCADE
)
''')


planes_data = [
    (1, 'Boeing', '737', 2000),
    (2, 'Airbus', 'A320', 3000),
    (3, 'Boeing', '747', 4000),
    (4, 'Airbus', 'A380', 6000),
    (5, 'Embraer', 'E190', 1500),
    (6, 'Bombardier', 'CRJ900', 1400),
    (7, 'Cessna', 'C172', 900),
    (8, 'Piper', 'PA-28', 800),
    (9, 'McDonnell Douglas', 'MD-80', 2500),
    (10, 'Dassault', 'Falcon 900', 5000)
]
cursor.executemany('INSERT INTO planes (id, type, model, max_cargo) VALUES (?, ?, ?, ?)', planes_data)

airports_data = [
    (1, 'Международный аэропорт Шереметьево', 'Москва'),
    (2, 'Международный аэропорт Домодедово', 'Москва'),
    (3, 'Аэропорт Пулково', 'Санкт-Петербург'),
    (4, 'Международный аэропорт Внуково', 'Москва'),
    (5, 'Международный аэропорт Казань', 'Казан'),
    (6, 'Международный аэропорт Сочи', 'Сочи'),
    (7, 'Аэропорт Кольцово', 'Екатеринбург'),
    (8, 'Аэропорт Стригино', 'Нижний Новгород'),
    (9, 'Международный аэропорт Владивосток', 'Владивосток'),
    (10, 'Международный аэропорт Иркутск', 'Иркутск'),
]
cursor.executemany('INSERT INTO airports (id, name, city) VALUES (?, ?, ?)', airports_data)

tickets_data = [
    (1, 'Москва - Санкт-Петербург', 'Москва', 1, 1, '2023-10-15', 90, 120.50),
    (2, 'Москва - Казань', 'Казан', 5, 2, '2023-10-16', 85, 150.00),
    (3, 'Москва - Сочи', 'Сочи', 6, 3, '2023-10-17', 110, 200.00),
    (4, 'Санкт-Петербург - Сочи', 'Сочи', 6, 4, '2023-10-18', 120, 250.00),
    (5, 'Москва - Екатеринбург', 'Екатеринбург', 7, 5, '2023-10-19', 145, 300.00),
    (6, 'Казань - Владивосток', 'Владивосток', 9, 6, '2023-10-20', 180, 350.00),
    (7, 'Сочи - Иркутск', 'Иркутск', 10, 7, '2023-10-21', 200, 400.00),
    (8, 'Москва - Нижний Новгород', 'Нижний Новгород', 8, 8, '2023-10-22', 90, 130.00),
    (9, 'Санкт-Петербург - Казань', 'Казан', 5, 9, '2023-10-23', 95, 160.00),
    (10, 'Москва - Сочи', 'Сочи', 6, 10, '2023-10-24', 110, 220.00),
]
cursor.executemany('INSERT INTO tickets (id, route, point, id_i, id_p, flight_date, duration, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', tickets_data)

clients_data = [
    (1, 1, 'Иванов', 'Иван', 'Иванович', 'Ленина 1', 'Москва', 0, '2023-10-10'),
    (2, 2, 'Петров', 'Петр', 'Петрович', 'Кремль 12', 'Москва', 5, '2023-10-11'),
    (3, 3, 'Сидоров', 'Сидор', 'Сидорович', 'Пушкина 5', 'Санкт-Петербург', 10, '2023-10-12'),
    (4, 4, 'Смирнов', 'Алексей', 'Сергеевич', 'Мира 15', 'Екатеринбург', 0, '2023-10-13'),
    (5, 5, 'Кузнецов', 'Дмитрий', 'Дмитриевич', 'Центральная 6', 'Казан', 20, '2023-10-14'),
    (6, 6, 'Новиков', 'Андрей', 'Владимирович', 'Башкирская 7', 'Сочи', 0, '2023-10-15'),
    (7, 7, 'Орлов', 'Олег', 'Олегович', 'Городская 8', 'Владивосток', 0, '2023-10-16'),
    (8, 8, 'Васильев', 'Василий', 'Васильевич', 'Октябрьская 9', 'Нижний Новгород', 15, '2023-10-17'),
    (9, 9, 'Фёдоров', 'Фёдор', 'Фёдорович', 'Советская 10', 'Иркутск', 0, '2023-10-18'),
    (10, 10, 'Александров', 'Александр', 'Александрович', 'Чапаева 11', 'Казан', 0, '2023-10-19'),
]
cursor.executemany('INSERT INTO clients (id, id_a, Lname, Fname, patronymic, adress, city, discount, order_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', clients_data)


cursor.execute('SELECT * FROM planes')
plane = cursor.fetchall()
print("Авиабилеты:")
for z in plane:
    print(z)

cursor.execute('SELECT * FROM airports')
airport = cursor.fetchall()
print("Авиабилеты:")
for a in airport:
    print(a)
    
cursor.execute('SELECT * FROM tickets')
ticket = cursor.fetchall()
print("Авиабилеты:")
for t in ticket:
    print(t)

cursor.execute('SELECT * FROM clients')
users = cursor.fetchall()
print("Клиенты:")
for client in users:
    print(client)

connection.commit()
connection.close()
