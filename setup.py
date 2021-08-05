import cruid
from json import loads


names = cruid.DataBase()

names.delete("names")
names.delete("rankings")
names.delete("gamedata")

names.create("names", {
    "letter": "TEXT",
    "words": "TEXT"
})

with open("words.json", "r") as fh:
    data = loads(fh.read())

for key in data.keys():
    names.insert("names", [key, data[key]])
    # TODO: згенерувати список слів variants.txt
