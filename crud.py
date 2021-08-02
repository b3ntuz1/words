import sqlite3


class DataBase:
    """
    Мідлварь для роботи з БД. Імплементує бозові операці CREATE, READ, UPDATE та DELETE.
    За замовчування використовується sqlite3
    """

    def __init__(self, db_name="gamedata.db"):
        self.db = sqlite3.connect(db_name)
        self.db.row_factory = sqlite3.Row

    def __del__(self):
        self.db.close()

    def create(self, table, data):
        """
        Створить нову таблицю.
        table -- імʼя таблиці
        data -- структура таблиці котра представлена словарем де ключ це назва поля, а значення це тип
        """
        command = [f"CREATE TABLE IF NOT EXISTS {table}("]
        for k in data.keys():
            command.append(f"{k} {data[k]},")

        # обʼєднати все в одну sql команду та забрати зайву кому
        self.db.execute("".join(command)[:-1] + ");")

    def read(self, table_name, row='*') -> list:
        """
        Поверне вміст table_name. Якщо вказаний row, то тільки дані для row
        return: стисок рядків де дані з таблиці розділені комами або пустий список
        """
        cur = self.db.execute(f"SELECT {row} FROM {table_name}")
        data = []
        for i in cur.fetchall():
            data.append(", ".join(i))
        return data

    def update(self):
        pass

    def delete(self):
        pass
