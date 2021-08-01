import sqlite3


class DataBase:
    """
    Мідлварь для роботи з БД. Імплементує бозові операці CREATE, READ, UPDATE та DELETE.
    За замовчування використовується sqlite3
    """

    def __init__(self, db_name="gamedata.db"):
        self.db = sqlite3.connect(db_name)

    def __del__(self):
        self.db.close()

    def create(self, table, data):
        """
        Створить нову таблицю.
        table -- імʼя таблиці
        data -- структура таблиці котра представлена словарем де ключ це назва поля, а значення це тип
        """
        command = [f"CREATE TABLE {table}("]
        for k, v in data:
            command.append(f"{k}, {v}")
        command.append(");")
        self.db.execute("".join(command))

    def read(self, table_name, data='*') -> dict:
        """
        Прочитати data із table_name
        """

        return dict

    def update(self):
        pass

    def delete(self):
        pass
