from json import loads
from os import remove
from os.path import exists
# видалити стару БД
if exists("gamedata.db"):
    remove("gamedata.db")


# імпорти мали б бути вище, але інакше не працює видалення файлу з БД
from models import Words, GameData, Rankings, UsedWords


# підключитися до БД
words = Words()
gamedata = GameData()
rankings = Rankings()
used_words = UsedWords()

# створити нові таблиці
words.create_table()
gamedata.create_table()
rankings.create_table()
used_words.create_table()

# заповнити таблиці
gamedata.last_user = "_"
gamedata.current_letter = ""
gamedata.words = ""
gamedata.save()

# завантажити дані із .json файлу
with open("words.json", "r") as fh:
    raw_data = loads(fh.read())

# зберегти та закінчити роботу
for k, v in sorted(raw_data.items()):
    Words(letter=k, word_lists=v).save()
    UsedWords(letter=k, word_lists="").save()
