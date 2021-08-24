from peewee import DoesNotExist
from models import Rankings, GameData, UsedWords, Words


def update_rankings(user):
    """
    Оновити рейтингову таблицю
    """
    # for existing user
    for usr in Rankings.select():
        if usr.user == user:
            usr.count += 1
            usr.save()
            return 0

    # for new user
    ranks = Rankings()
    ranks.user = user
    ranks.count = 1
    ranks.save()
    return None


def update_gamedata(user, word):
    """
    Оновити збережену гру.
    """
    try:
        gamedata = GameData.get()
    except DoesNotExist:
        gamedata = GameData()

    words = remove_used_words(word[-1])

    # update gamedata
    gamedata.last_user = user
    gamedata.current_letter = word[-1]
    gamedata.words = ", ".join(words)
    gamedata.save()


def update_used_words(word):
    """
    Метод не перевіряє на валідність слова.
    Він тільки додає їх до БД.
    """
    used_words = UsedWords().get(UsedWords.letter == word[0])
    used_words.word_lists += word + ", "
    used_words.save()


def purify(dirty_word):
    """
    Очищає від пробільних символів та конвертурє в lowercase
    """
    purify = dirty_word.strip().lower()
    for i in ",.[]_()'":
        purify = purify.replace(i, '')

    if not purify:
        raise ValueError("Не може бути пустий рядок")
    return purify


def get_word_lists(letter, model) -> str:
    """
    Поверне список слів із таблиці model
    """
    if model.table_exists():
        return model.get(model.letter == letter).word_lists
    return " "


def clear_db():
    """ Очищає базу """
    ranks = Rankings()
    ranks.drop_table(save=True)
    ranks.create_table()

    gamedata = GameData()
    gamedata.drop_table(save=True)
    gamedata.create_table()

    used_words = UsedWords().select()
    for letter in used_words:
        letter.word_lists = ""
        letter.save()


def remove_used_words(letter) -> list:
    """
    виключити використані слова із загального списку слів
    """
    words = get_word_lists(letter, Words).split(', ')
    used_words = get_word_lists(letter, UsedWords).split(', ')
    for i in used_words:
        if not i:
            continue
        if i in words:
            words.remove(i)
    return words
