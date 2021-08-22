"""
Згенерувати список покемонів із сторінки
https://gamepress.gg/pokemongo/pokemon-list
"""

from urllib.request import urlopen, Request
from lxml import html
import json

url = "https://gamepress.gg/pokemongo/pokemon-list"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"  # noqa E501
}
raw_data = urlopen(Request(url, headers=headers))
tree = html.fromstring(raw_data.read())
result = {}
for el in tree.cssselect("#pokemon-list")[0].getchildren():
    # отримати тільки перше слово, яке повинне бути іменем покемона
    pkm_name = el.attrib['data-name'].strip().split(" ")[0]
    pkm_name = pkm_name.replace("é", "e").replace("\u2640", "").replace("\u2642", "").lower()

    letter = pkm_name[0].lower()
    if letter.isdigit():
        continue
    if result.get(letter) == None:
        result[letter] = ", "

    # перевірка на унікальність імен
    # якщо у списку немає цього імені, то додати
    if pkm_name not in result.get(letter).split(', '):
        result[letter] += pkm_name + ", "

for k, v in result.items():
    result[k] = v[2:-2]

with open("words.json", "w") as fh:
    fh.writelines(json.dumps(result))
