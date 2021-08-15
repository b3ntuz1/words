# -*- coding: utf-8 -*-
from random import Random
import models
from en_lang import TextsForGame
from peewee import DoesNotExist


class Words:
    def __init__(self):
        self.text = TextsForGame()

    def start_game(self):
        # почати гру з пустими таблицями
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

    def rankings(self) -> str:
        """ Турнірна таблиця. Вирівнювання по найдовшому слову. """
        ranks = models.Rankings.select()  # прочитати турнірну таблицю
        # TODO: написати метод для видачі рейтингу
        pass

    def check(self, user, answer):
        """ Перевірити чи підходить відповідь """
        answer = self.purify(answer)
        gamedata = models.GameData.get()

        if gamedata.last_user == user:
            return self.text.user_cant_move.format(user=user)

        if answer in self.get_word_lists(answer[0], models.UsedWords):
            return self.text.used_word

        if gamedata.current_letter != answer[0]:
            return self.text.next_word_starts_with.format(letter=gamedata.current_letter)

        if answer not in self.get_word_lists(answer[0], models.Words):
            return self.text.wrong_answer

        # update data
        self.update_rankings(user)
        self.update_gamedata(user, answer)
        self.update_used_words(answer)

        count = len(models.GameData.get().words.split(', '))
        return self.text.correct_answer.format(letter=answer[-1], count=count)

    def update_rankings(self, user):
        # for existing user
        for u in models.Rankings.select():
            if u.user == user:
                u.count += 1
                u.save()
                return 0

        # for new user
        ranks = models.Rankings()
        ranks.user = user
        ranks.count = 1
        ranks.save()

    def update_gamedata(self, user, word):
        # get gamedata
        try:
            gamedata = models.GameData.get()
        except DoesNotExist:
            gamedata = models.GameData()

        # виключити використані слова із загального списку слів
        words = self.get_word_lists(word[-1], models.Words).split(', ')
        used_words = self.get_word_lists(word[-1], models.UsedWords).split(', ')
        for i in used_words:
            if i == '':
                continue
            if i in words:
                words.remove(i)

        # update gamedata
        gamedata.last_user = user
        gamedata.current_letter = word[-1]
        gamedata.words = ", ".join(words)
        gamedata.save()

    def update_used_words(self, word):
        """
        Метод не перевіряє на валідність слова.
        Він тільки додає їх до БД.
        """
        uw = models.UsedWords().get(models.UsedWords.letter == word[0])
        uw.word_lists += word + " "
        uw.save()

    def purify(self, dirty_word):
        """
        Очищає від пробільних символів та конвертурє в lowercase
        """
        purify = dirty_word.strip().lower()
        for i in ",.[]_()'":
            purify = purify.replace(i, '')
        
        if len(purify) == 0:
            raise ValueError("Не може бути пустий рядок")
        return purify

    def get_word_lists(self, letter, model) -> str:
        if model.table_exists():
            return model.get(model.letter == letter).word_lists
        return " "

    def clear_db(self):
        """ Очищає базу перед новою грою """
        r = models.Rankings()
        r.drop_table(save=True)
        r.create_table()

        d = models.GameData()
        d.drop_table(save=True)
        d.create_table()

        uw = models.UsedWords().select()
        for t in uw:
            t.word_lists = ""
            t.save()
