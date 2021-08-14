# -*- coding: utf-8 -*-
import unittest
import words
import models

class TestWords(unittest.TestCase):
    def setUp(self):
        self.game = words.Words()

    def tearDown(self):
        self.game.clear_db()

    def test_start_game(self):
        self.assertIsInstance(self.game.start_game(), str)

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
