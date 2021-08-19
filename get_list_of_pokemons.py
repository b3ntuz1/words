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
    pkm_name = el.attrib['data-name'].strip()
    if len(pkm_name.split(" ")) > 1:
        continue
    pkm_name = pkm_name.replace("é", "e").lower()
    letter = pkm_name[0].lower()
    if result.get(letter):
        result[letter] += ', ' + pkm_name
        continue
    result[letter] = pkm_name

with open("words.json", "w") as fh:
    fh.writelines(json.dumps(result))
