# -*- coding: utf-8 -*-
from random import Random
import models
from peewee import DoesNotExist


class Words:
    def start_game(self):
        # почати гру з пустими таблицями
        self.clear_db()

        # прочитати список слів
        with open("variants.txt") as fh:
            wlist = fh.readlines()

        # випадкове слово
        random_word = wlist[Random().randint(0, len(wlist) - 1)].strip()
        random_word = self.purify(random_word)

        return f"[start_game] start word is: {random_word}"
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
            return f"{user} can't move"
        if gamedata.current_letter != answer[0]:
            return f"Next word should start with {gamedata.current_letter}"
        if answer not in self.get_word_lists(answer[0], models.Words):
            return f"You answer is wrong"
        else:
            return f"[answer] {answer}, [user] {user}"

        if answer in self.get_word_lists(answer[0], models.UsedWords):
            return f"Вже було це слово. Спробуйте ще раз."

        # update data
        self.update_rankings(user)
        self.update_gamedata(user, answer)
        self.update_used_words(answer)

    def update_rankings(self, user):
        for u in models.Rankings.select():
            if u.user == user:
                u.count += 1
                u.save()
                return f"[update_rankings] {u.user} have {u.count} points"

        ranks = models.Rankings()
        ranks.user = user
        ranks.count = 1
        ranks.save()
        return f"[update_rankings] create {ranks.user} with {ranks.count}"

    def update_gamedata(self, user, word):
        # get gamedata
        try:
            gamedata = models.GameData.get()
        except DoesNotExist:
            gamedata = models.GameData()

        # update gamedata
        gamedata.last_user = user
        gamedata.current_letter = word[-1]
        gamedata.words = self.get_word_lists(word[-1], models.Words)
        gamedata.save()

        return(f"[update_gamedata] {user}, {word}. Next letter is {word[-1]}")

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
        if len(purify) == 0:
            raise ValueError("Не може бути пустий рядок")
        return purify

    def get_word_lists(self, letter, model):
        if model.table_exists():
            return model.get(model.letter == letter).word_lists
        return ""

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


if __name__ == '__main__':
    w = Words()
    print(24 * "-")
    # print(w.start_game())
    print(w.check("user", "rattata"))
    print(w.rankings())
    # print("onix" in w.get_word_lists('o', models.UsedWords))
    # print(w.get_word_lists('p', models.UsedWords))
    print(24 * "-")
