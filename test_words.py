# -*- coding: utf-8 -*-
import unittest
import words
import models
from en_lang import TextsForGame
from peewee import DoesNotExist

class TestWords(unittest.TestCase):
    def setUp(self):
        self.game = words.Words()
        self.text = TextsForGame()

    def tearDown(self):
        self.game.clear_db()

    def test_start_game(self):
        data = self.game.start_game()
        self.assertIsInstance(data, str)
        gamedata = models.GameData.get()
        self.assertEqual(gamedata.last_user, "_")
        self.assertEqual(gamedata.current_letter, data[-1])

    def test_check_error_texts(self):
        word = self.game.start_game()
        answer = word[-1] + "_python"
        wlist = models.GameData.get().words.split(', ')

        self.assertEqual(self.game.check("_", "python"),
            self.text.user_cant_move.format(user="_")
            )
        self.assertEqual(self.game.check("Gvido", "_python"),
            self.text.next_word_starts_with.format(letter=word[-1])
            )
        self.assertEqual(self.game.check("Gvido", answer),
            self.text.wrong_answer
            )
        self.assertEqual(self.game.check("Gvido", word),
            self.text.used_word
            )
        self.assertEqual(self.game.check("Gvido", wlist[0]),
            self.text.correct_answer.format(letter=wlist[0][-1],
            count=len(models.GameData.get().words.split(', ')))
            )

    @unittest.skip("Not implemented yet")
    def test_check(self):
        pass

    @unittest.skip("Not implemented yet")
    def test_rankings(self):
        pass

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
                self.game.update_rankings(i)
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
                self.game.update_gamedata(i, j)
                gd = models.GameData.get()
                self.assertEqual(gd.last_user, i)
                self.assertNotIn(j, gd.words)
                self.assertEqual(gd.current_letter, j[-1])

    def test_uuw(self):
        testdata = [
            ("pikachu", "pikachu "),
            ("raichu", "raichu "),
            ("vaporeon", "vaporeon "),
            ("pichu", "pikachu pichu ")
        ]
        for k, v in testdata:
            with self.subTest(k):
                self.game.update_used_words(k)
                w = models.UsedWords.get(models.UsedWords.letter == k[0]).word_lists
                self.assertEqual(w, v)

    def test_purify(self):
        for i in [" pikachu ", " Pikachu", "pIkachU", "    Pikachu"]:
            with self.subTest(i):
                self.assertEqual(self.game.purify(i), "pikachu")

    def test_purify_fail(self):
        with self.assertRaises(ValueError):
            self.game.purify("")

    def test_get_wl(self):
        l = self.game.get_word_lists("x", models.Words)
        self.assertEqual(l, "xatu, xerneas")

if __name__ == "__main__":
    unittest.main()
