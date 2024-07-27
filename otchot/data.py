import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta


# Функция для генерации данных о клиентах
def generate_clients(num_clients):
    return pd.DataFrame({
        'идентификатор_клиента': range(1000, 1000 + num_clients),
        'имя_клиента': [f'Клиент {i}' for i in range(1, num_clients + 1)],
        'адрес_клиента': [f'Адрес {i}' for i in range(1, num_clients + 1)]
    })


# Функция для генерации случайных дат в пределах месяца
def random_dates_for_month(start, end, num_records):
    delta = end - start
    return [start + timedelta(days=random.randint(0, delta.days)) for _ in range(num_records)]


# Функция для генерации данных о перевозках
def generate_shipments_data(num_records, num_clients=10):
    routes = ['Маршрут A', 'Маршрут B', 'Маршрут C', 'Маршрут D']
    cargos = ['Электроника', 'Одежда', 'Еда', 'Мебель']

    start_date = datetime(2023, 7, 1)
    end_date = datetime(2023, 7, 31)

    # Создание данных о клиентах
    clients_df = generate_clients(num_clients)

    # Генерация данных о перевозках
    data = {
        'идентификатор_отгрузки': range(1, num_records + 1),
        'идентификатор_клиента': [random.choice(clients_df['идентификатор_клиента']) for _ in range(num_records)],
        'идентификатор_контейнера': [random.randint(10000, 10050) for _ in range(num_records)],
        'маршрут': random.choices(routes, k=num_records),
        'дата_и_время_отправления': random_dates_for_month(start_date, end_date, num_records),
        'дата_и_время_прибытия': random_dates_for_month(start_date, end_date, num_records),
        'тип_груза': random.choices(cargos, k=num_records),
        'вес_груза': np.random.uniform(5, 25, num_records),  # Тонны
        'объем_груза': np.random.uniform(10, 30, num_records),  # Кубометры
        'вместимость_контейнера': [30] * num_records,
        'стоимость': np.random.uniform(500, 5000, num_records) * 100,  # USD
        'доход': np.random.uniform(1000, 10000, num_records)* 100  # USD
    }

    df = pd.DataFrame(data)
    df['дата_и_время_прибытия'] = df.apply(
        lambda row: row['дата_и_время_отправления'] + timedelta(hours=random.uniform(10, 100)), axis=1)
    df['коэффициент_заполнения'] = df['объем_груза'] / df['вместимость_контейнера']

    # Объединение с данными о клиентах для получения имен клиентов
    df = df.merge(clients_df[['идентификатор_клиента', 'имя_клиента']], on='идентификатор_клиента', how='left')

    # Удаление столбца идентификатора клиента
    df.drop(columns=['идентификатор_клиента'], inplace=True)

    df.to_csv('shipments_data.csv', index=False)


# Пример использования
generate_shipments_data(num_records=100)
