# -*- coding: utf-8 -*-
"""
Реалізаці гри в слова для чатів, як телеграм
"""
import difflib
from random import Random
from models import Rankings, GameData, UsedWords, Words
from en_lang import TextsForGame
from libgame import *


class WordsGame:
    """
    Гра в слова
    """

    def __init__(self):
        self.text = TextsForGame()

    def start_game(self, start_word="") -> str:
        """
        Починає гру створюючи відповідні таблиці в БД
        та вибирає стартове слово
        return: str слово з якого почнеться гра
        """
        clear_db()

        # прочитати список слів
        with open("variants.txt") as fh:
            wlist = fh.readlines()

        # випадкове слово
        if start_word:
            random_word = start_word
        else:
            random_word = wlist[Random().randint(0, len(wlist) - 1)].strip()
        random_word = purify(random_word)

        update_gamedata("_", random_word)
        update_used_words(random_word)
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
        answer = purify(answer)
        gamedata = GameData.get()

        # заблокований користувач
        if gamedata.last_user == user:
            return self.text.user_cant_move.format(user=user)

        # використані слова
        if answer in get_word_lists(answer[0], UsedWords):
            return self.text.used_word

        # слово починається з неправельної букви
        if gamedata.current_letter != answer[0]:
            return self.text.next_word_starts_with.format(letter=gamedata.current_letter)

        # виправлення неправельний слів
        if answer not in get_word_lists(answer[0], Words):
            words_list = remove_used_words(answer[0])
            if words_list:
                diff = difflib.get_close_matches(answer, words_list)
                if diff:
                    ratio = difflib.SequenceMatcher(None, diff[0], answer).ratio()
                    if ratio > 0.7:
                        return self.text.maybe_you_meant.format(word=diff[0])

            return self.text.wrong_answer

        # update data
        update_rankings(user)
        update_used_words(answer)
        update_gamedata(user, answer)

        # game over
        count = GameData.get().words
        if not count:
            return self.text.game_over

        result = self.text.correct_answer.format(letter=answer[-1], count=len(count.split(', ')))
        return result

    def hint(self, letter, hint=True):
        """ Виводить підказку """
        words = get_word_lists(letter, Words).split(', ')
        used_words = get_word_lists(letter, UsedWords)
        sequens = [i for i in words if i not in used_words]
        sequens = sequens[Random().randint(0, len(sequens) - 1)]
        result = sequens[0] + sequens[1]
        for i in range(2, len(sequens)):
            if i % 2 == 0:
                result += sequens[i]
            else:
                result += '_'
        if hint:
            return result
        return sequens
