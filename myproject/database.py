import sqlite3
from typing import List, Tuple

class Db:
    def __init__(self, db_name: str = 'tasks.db'):
        # Подключение к базе данных
        self.conn = sqlite3.connect(db_name)
        # Создание таблицы задач, если она не существует
        self.create_table()

    def create_table(self):
        # Создание таблицы tasks с полями id, task, is_completed и user_id
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    is_completed BOOLEAN NOT NULL CHECK (is_completed IN (0, 1)),
                    user_id INTEGER NOT NULL
                )
            """)

    def add_task(self, task: str, user_id: int):
        # Добавление новой задачи в таблицу tasks
        with self.conn:
            self.conn.execute("INSERT INTO tasks (task, is_completed, user_id) VALUES (?, 0, ?)", (task, user_id))

    def remove_task(self, task_id: int, user_id: int):
        # Удаление задачи из таблицы tasks по id задачи и id пользователя
        with self.conn:
            self.conn.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))

    def complete_task(self, task_id: int, user_id: int):
        # Обновление статуса задачи на выполненную (is_completed = 1) по id задачи и id пользователя
        with self.conn:
            self.conn.execute("UPDATE tasks SET is_completed = 1 WHERE id = ? AND user_id = ?", (task_id, user_id))

    def list_tasks(self, user_id: int) -> List[Tuple[int, str, bool]]:
        # Получение списка задач для конкретного пользователя
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, task, is_completed FROM tasks WHERE user_id = ?", (user_id,))
        return cursor.fetchall()
