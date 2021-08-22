# -*- coding: utf-8 -*-
"""
Реалізаці гри в слова для чатів, як телеграм
"""
import difflib
from random import Random
from peewee import DoesNotExist
from models import Rankings, GameData, UsedWords, Words
from en_lang import TextsForGame


class WordsGame:
    """
    Гра в слова
    """
    def __init__(self):
        self.text = TextsForGame()

    def start_game(self) -> str:
        """
        Починає гру створюючи відповідні таблиці в БД
        та вибирає стартове слово
        return: str слово з якого почнеться гра
        """
        self.clear_db()

        # прочитати список слів
        with open("variants.txt") as fh:
            wlist = fh.readlines()

        # випадкове слово
        random_word = wlist[Random().randint(0, len(wlist) - 1)].strip()
        random_word = self.purify(random_word)

        self.update_gamedata("_", random_word)
        self.update_used_words(random_word)
        return random_word

    @staticmethod
    def rankings() -> str:
        """ Турнірна таблиця. Вирівнювання по найдовшому імені. """
        table = {}
        space = 0
        for i in Rankings.select().order_by(Rankings.count.desc()):
            table[i.user] = i.count
            if space < len(i.user):
                space = len(i.user)
        result = []
        for k, v in table.items():
            result.append(f"{k}{abs(space - len(k)) * ' '} | {v}")
        return "\n".join(result)

    def check(self, user, answer):
        """ Перевірити чи підходить відповідь """
        answer = self.purify(answer)
        gamedata = GameData.get()

        if gamedata.last_user == user:
            return self.text.user_cant_move.format(user=user)

        if answer in self.get_word_lists(answer[0], UsedWords):
            return self.text.used_word

        if gamedata.current_letter != answer[0]:
            return self.text.next_word_starts_with.format(letter=gamedata.current_letter)

        if answer not in self.get_word_lists(answer[0], Words):
            diff = difflib.get_close_matches(answer, self.remove_used_words(answer[0]))[0]
            if difflib.SequenceMatcher(None, diff, answer).ratio() > 0.7:
                return f"Мaybe you meant **{diff}**"
            return self.text.wrong_answer

        # update data
        self.update_rankings(user)
        self.update_used_words(answer)
        self.update_gamedata(user, answer)

        # game over
        count = GameData.get().words
        if not count:
            return self.text.game_over

        result = self.text.correct_answer.format(letter=answer[-1], count=len(count.split(', ')))
        return result

    @staticmethod
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

    def update_gamedata(self, user, word):
        """
        Оновити збережену гру.
        """
        try:
            gamedata = GameData.get()
        except DoesNotExist:
            gamedata = GameData()

        words = self.remove_used_words(word[-1])

        # update gamedata
        gamedata.last_user = user
        gamedata.current_letter = word[-1]
        gamedata.words = ", ".join(words)
        gamedata.save()

    @staticmethod
    def update_used_words(word):
        """
        Метод не перевіряє на валідність слова.
        Він тільки додає їх до БД.
        """
        used_words = UsedWords().get(UsedWords.letter == word[0])
        used_words.word_lists += word + ", "
        used_words.save()

    @staticmethod
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

    @staticmethod
    def get_word_lists(letter, model) -> str:
        """
        Поверне список слів із таблиці model
        """
        if model.table_exists():
            return model.get(model.letter == letter).word_lists
        return " "

    @staticmethod
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

    def remove_used_words(self, letter) -> list:
        """
        виключити використані слова із загального списку слів
        """
        words = self.get_word_lists(letter, Words).split(', ')
        used_words = self.get_word_lists(letter, UsedWords).split(', ')
        for i in used_words:
            if not i:
                continue
            if i in words:
                words.remove(i)
        return words
