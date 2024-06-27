import sqlite3


def connection_to_database():
    # Підключення до бази даних
    conn = sqlite3.connect('C:/Users/user/PycharmProjects/cafe_ordering_system_bot/database.db')

    # Створення курсору
    cursor = conn.cursor()

    # Виконання запиту
    query = "SELECT dish_name, dish_price FROM Menu WHERE category = 'Закуски';"
    cursor.execute(query)

    # Витяг даних
    results = cursor.fetchall()

    # Закриття курсору та з'єднання
    cursor.close()
    conn.close()

    return results


# Виклик функції та обробка результатів
results = connection_to_database()
for row in results:
    print(row)
for dish_name, dish_price in results:
    print(f"Название блюда: {dish_name}, Цена: {dish_price}")
