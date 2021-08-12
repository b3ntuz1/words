# -*- coding: utf-8 -*-
import unittest
import words

class TestWords(unittest.TestCase):
    def setUp(self):
        self.game = words.Words()

    def test_startup_game(self):
        pass

    def test_rankings(self):
        pass

    def test_check(self):
        pass

    def test_update_rankings(self):
        pass

    def test_gamedata(self):
        pass

    def test_uuw(self):
        pass

    def test_purity(self):
        self.assertEqual(self.game.purify(" pikachu "), "pikachu")
        self.assertEqual(self.game.purify("Pikachu"), "pikachu")

    def test_get_wl(self):
        pass

    def test_clear_db(self):
        pass

if __name__ == "__main__":
    unittest.main()
