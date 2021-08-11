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

        print(f"[start_game] start word is: {random_word}")
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
            print(f"{user} can't move")
            return 0
        if gamedata.current_letter != answer[0]:
            print(f"Next word should start with {gamedata.current_letter}")
            return 0
        if answer not in self.get_word_lists(answer[0], models.Words):
            print(f"You answer is wrong")
            return 0
        else:
            print(f"[answer] {answer}")
            print(f"[user] {user}")

        # TODO: придумати як перевіряти використані слова
        if answer in self.get_word_lists(answer[0], models.UsedWords):
            print(f"Вже було це слово. Спробуйте ще раз.")
            return 0

        # update data
        self.update_rankings(user)
        self.update_gamedata(user, answer)
        self.update_used_words(answer)

    def update_rankings(self, user):
        for u in models.Rankings.select():
            if u.user == user:
                u.count += 1
                u.save()
                print(f"[update_rankings] {u.user} have {u.count} points")
                return 0

        ranks = models.Rankings()
        ranks.user = user
        ranks.count = 1
        ranks.save()
        print(f"[update_rankings] create {ranks.user} with {ranks.count}")

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

        print(f"[update_gamedata] {user}, {word}. Next letter is {word[-1]}")

    def update_used_words(self, word):
        uw = models.UsedWords().get(models.UsedWords.letter == word[0])
        uw.word_lists += word + " "
        uw.save()

        print(f"[update_used_words] add new word: {word}")

    def purify(self, dirty_word):
        purify = dirty_word.strip().lower()
        if len(purify) == 0:
            print(f"[purify] word length is zero")
            raise ValueError("Не може бути пустий рядок")
        return purify

    def get_word_lists(self, letter, model):
        return model.get(model.letter == letter).word_lists

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
