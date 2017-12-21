from bs4 import BeautifulSoup
from requests import get
from PIL import Image

# To generate images you need to install these:
# pip install bs4
# pip install requests
# pip install pil


# Where to save pics?
path = "pics/[file].png"
# File name format
file_name = "[id]_[name]"


positions = {}
f = open("items.txt", "r")
for i in f:
    t = i.split(": ")
    positions[t[0]] = t[1].replace("\n", "")


soup = BeautifulSoup(get("https://minecraft-ids.grahamedgecombe.com/").text, "html.parser")

items = soup.find_all("tr", {"class": "row"})
li = {}

img = Image.open(get("https://minecraft-ids.grahamedgecombe.com/images/sprites/items-27.png", stream=True).raw)

for a in items:
    pos = a.find("td", {"class": "row-icon"}).div["class"][1][6:]
    desc = a.find("td", {"class": "row-desc"}).span.text
    xy = positions[pos].split(" ")
    x = abs(int(xy[0]))
    y = abs(int(xy[1]))
    final = path.replace("[file]", file_name.replace("[id]", a.td.text.replace(":", "_")).replace("[name]", desc))
    img.crop((x, y, x + 32, y + 32)).save(final)
    li[a.td.text] = 0
