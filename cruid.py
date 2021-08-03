import sqlite3


class DataBase:
    """
    Мідлварь для роботи з БД. Імплементує бозові операці CREATE, READ,
    INSERT, UPDATE та DELETE.
    За замовчування використовується sqlite3
    """

    def __init__(self, db_name="gamedata.db"):
        self.db = sqlite3.connect(db_name)
        self.db.row_factory = sqlite3.Row

    def __del__(self):
        self.db.close()

    def create(self, table: str, data: dict):
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

    def read(self, table_name: str, col='*', where="") -> list:
        """
        Поверне вміст table_name. Якщо вказаний col, то тільки дані для цієї колонки
        return: стисок рядків де дані з таблиці розділені комами або пустий список
        """
        sql = f"SELECT {col} FROM {table_name}"
        if len(where) > 0:
            sql += f" WHERE {where}"
        cur = self.db.execute(sql)
        data = []
        for i in cur.fetchall():
            data.append(", ".join(i))
        return data

    def update(self):
        pass

    def insert(self, table_name: str, values: list):
        """
        Вставляє нові дані до таблиці. Важливо зберігаюти правильну послідовність
        значень котрі будуть додані в БД.
        Цей метод, це проста обгортка навколо INSERT INTO з SQL
        """
        data = ", ".join(map(lambda s: "'" + s.strip() + "'", values))
        self.db.execute(f"insert into {table_name} values ({data})")
        self.db.commit()

    def delete_row(self, table_name, where):
        """
        Видалить рядок з таблиці.
        """
        self.db.execute(f"delete from {table_name} where {where}")
        self.db.commit()

    def delete(self):
        """
        Видалить таблицю з БД.
        """
