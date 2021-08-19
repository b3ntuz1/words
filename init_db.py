from json import loads
from os import remove
from os.path import exists


def main():
    # видалити стару БД
    if exists("gamedata.db"):
        print("[setup] Remove old DB")
        remove("gamedata.db")

    # імпорти мали б бути вище, але інакше не працює видалення файлу з БД
    from models import Words, GameData, Rankings, UsedWords

    # підключитися до БД
    print("[setup] Connecting...")
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
    print("[setup] Read the json file")
    with open("words.json", "r") as fh:
        raw_data = loads(fh.read())

    # зберегти та закінчити роботу
    print("[setup] Filling DB")
    for k, v in sorted(raw_data.items()):
        Words(letter=k, word_lists=v).save()
        UsedWords(letter=k, word_lists="").save()


if __name__ == "__main__":
    main()
