# -*- coding: utf-8 -*-
import unittest
import words
import models
from en_lang import TextsForGame
from peewee import DoesNotExist


class TestWords(unittest.TestCase):
    def setUp(self):
        self.game = words.WordsGame()
        self.text = TextsForGame()

    def tearDown(self):
        words.clear_db()

    def test_start_game(self):
        data = self.game.start_game()
        self.assertIsInstance(data, str)
        gamedata = models.GameData.get()
        self.assertEqual(gamedata.last_user, "_")
        self.assertEqual(gamedata.current_letter, data[-1])

    def test_start_game_with_word(self):
        data = self.game.start_game(start_word="pikachu")
        self.assertEqual(data, "pikachu")

    def test_check_user_cant_move(self):
        self.game.start_game()
        self.assertEqual(self.game.check("_", "python"),
                         self.text.user_cant_move.format(user="_")
                         )

    def test_check_used_words(self):
        word = self.game.start_game()
        self.assertEqual(self.game.check("Gvido", word),
                         self.text.used_word
                         )

    def test_chech_wrond_answer(self):
        word = self.game.start_game()
        answer = word[-1] + "-python"
        self.assertEqual(self.game.check("Gvido", answer),
                         self.text.wrong_answer
                         )

    def test_check_next_word_start_with(self):
        word = self.game.start_game()
        self.assertEqual(self.game.check("Gvido", "_python"),
                         self.text.next_word_starts_with.format(letter=word[-1])
                         )

    def test_check_error_correct_answer(self):
        word = self.game.start_game()
        answer = word[-1] + "-python"
        wlist = models.GameData.get().words.split(', ')
        game_result = self.game.check("Gvido", wlist[0])
        count = len(models.GameData.get().words.split(', '))

        self.assertEqual(game_result, self.text.correct_answer.format(letter=wlist[0][-1], count=count))

    def test_check_game_over(self):
        start_game = self.game.start_game(start_word="munchlax")
        self.game.check("Gvido", "xerneas")
        self.game.check("Van", "steelix")
        self.game.check("Rossum", "xatu")
        self.game.check("Gvido", "unfezant")
        self.game.check("Van", "tropius")
        self.assertEqual(self.game.check("Gvido", "snorlax"),
                         self.text.game_over
                         )

    def test_meybe_you_mean(self):
        data = self.game.start_game(start_word="pikachu")
        self.assertEqual(
            self.game.check("Esh", "uxee"),
            self.text.maybe_you_meant.format(word="uxie")
        )

    def test_rankings(self):
        self.game.start_game()
        models.Rankings(user="test_user", count=1).save()
        models.Rankings(user="test", count=2).save()
        models.Rankings(user="Gvido_Van_Rossum", count=24).save()
        self.assertEqual(self.game.rankings(),
                         "Gvido_Van_Rossum | 24\ntest             | 2\ntest_user        | 1")

    def test_update_rankings(self):
        testdata = [
            ('unittest', 1),
            ('testuser', 1),
            ('unittest', 2),
            ('ash_katchup', 1),
            ('ash_katchup', 2)
        ]

        for i, j in testdata:
            with self.subTest(i):
                words.update_rankings(i)
                user = models.Rankings.get(models.Rankings.user == i)
                self.assertEqual(user.user, i)
                self.assertEqual(user.count, j)

    def test_gamedata(self):
        testdata = [
            ('unittest', 'lugia'),
            ('testuser', 'raichu'),
            ('unittest', 'togepi'),
            ('ash_katchup', 'pikachu')
        ]
        for i, j in testdata:
            with self.subTest(i):
                words.update_gamedata(i, j)
                gd = models.GameData.get()
                self.assertEqual(gd.last_user, i)
                self.assertNotIn(j, gd.words)
                self.assertEqual(gd.current_letter, j[-1])

    def test_uuw(self):
        testdata = [
            ("pikachu", "pikachu, "),
            ("raichu", "raichu, "),
            ("vaporeon", "vaporeon, "),
            ("pichu", "pikachu, pichu, ")
        ]
        for k, v in testdata:
            with self.subTest(k):
                words.update_used_words(k)
                w = models.UsedWords.get(models.UsedWords.letter == k[0]).word_lists
                self.assertEqual(w, v)

    def test_purify(self):
        for i in [" pikachu ", " Pikachu", "pIkachU", "    Pikachu"]:
            with self.subTest(i):
                self.assertEqual(words.purify(i), "pikachu")

    def test_purify_fail(self):
        with self.assertRaises(ValueError):
            words.purify("")

    def test_get_wl(self):
        lst = words.get_word_lists("x", models.Words)
        self.assertEqual(lst, "xatu, xerneas")

    def test_hint(self):
        # get all words
        used_words = models.Words.get(models.Words.letter == 'p').word_lists.split(', ')

        # update used words
        uw = models.UsedWords.get(models.UsedWords.letter == 'p')
        uw.word_lists = used_words[:-1]
        uw.save()

        self.assertEqual(used_words[-1], self.game.hint(letter='p', hint=False))


if __name__ == "__main__":
    unittest.main()
