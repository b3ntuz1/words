import cruid
from random import Random


class Words:
    def __init__(self):
        self.db = cruid.DataBase()

    def start_game(self) -> str:
        # почати гру з пустими таблицями
        self.db.delete("rankings")
        self.db.create("rankings", {
            "user": "TEXT",
            "value": "INTEGER"
        })
        self.db.delete("gamedata")
        self.db.create("gamedata", {
            "last_user": "TEXT",
            "letter": "TEXT",
            "words": "TEXT"
        })

        # прочитати список слів
        with open("variants.txt") as fh:
            wlist = fh.readlines()

        # випадкове слово
        random_word = wlist[Random().randint(0, len(wlist) - 1)].strip()
        letter = random_word[-1].lower()
        data = self.db.read("names", where=f"letter=\"{letter}\"")
        self.db.insert(
            "gamedata",
            ["_", letter, data[0].split('|')[1]]
        )
        return random_word

    def rankings(self):
        """ Турнірна таблиця. Вирівнювання по найдовшому слову. """
        ranks = self.db.read("rankings")
        if len(ranks) == 0:
            return "Nothing here"
        result = []
        pmax0 = 0
        pmax1 = 0
        for i in ranks:
            parts = i.split('|')
            if pmax0 < len(parts[0]):
                pmax0 = len(parts[0])
            if pmax1 < len(parts[1]):
                pmax1 = len(parts[1])

        for i in ranks:
            blanks0 = ' '
            blanks1 = ' '
            parts = i.split('|')
            result.append(f"{(pmax0 + pmax1) * '-'}---")
            if len(parts[0]) < pmax0:
                blanks0 = (pmax0 - len(parts[0])) * " "
            if len(parts[1]) < pmax1:
                blanks1 = (pmax1 - len(parts[1])) * " "
            result.append(f"{parts[0]}{blanks0}|{blanks1}{parts[1]}\n")
        return "\n".join(result)


if __name__ == '__main__':
    w = Words()
    # print(w.start_game())
    print(w.rankings())
