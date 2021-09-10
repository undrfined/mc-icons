from bs4 import BeautifulSoup
from requests import get
from PIL import Image
import tinycss
import re

# To generate images you need to install these:
# pip install bs4
# pip install requests
# pip install pil
# pip install tinycss


# Where to save pics?
path = "pics/[file].png"
# File name format
file_name = "[id]_[name]"


# -----------------------------------------------------


base_url = "https://minecraft-ids.grahamedgecombe.com/"
base_url_html = get(base_url).text
parser = tinycss.make_parser('page3')

soup = BeautifulSoup(base_url_html, "html.parser")
items = soup.find_all("tr", {"class": "row"})
stylesheets = [base_url + style["href"]
               for style in soup.select('link[rel="stylesheet"]')]
sprite_sheet_url = None

positions = {}
li = {}

for sheet in stylesheets:
    data = get(sheet).text
    style = parser.parse_stylesheet(data)
    for rule in style.rules:
        selector = rule.selector.as_css()  # selector name (i.e. .items-*-*-*)
        if re.search(r'.items-', selector[:7]):
            [url, x, y, _] = rule.declarations[2].value.as_css().split(" ")

            positions[selector[7:]] = (
                abs(int(x.replace("px", ""))),
                abs(int(y.replace("px", "")))
            )

            if (sprite_sheet_url == None):
                sprite_sheet_url = base_url + url[4:-1]

if (sprite_sheet_url):
    img = Image.open(get(sprite_sheet_url, stream=True).raw)
    for a in items:
        pos = a.find("td", {"class": "row-icon"}).div["class"][1][6:]
        desc = a.find("td", {"class": "row-desc"}).span.text
        [x, y] = positions[pos]
        final = path.replace("[file]", file_name.replace(
            "[id]", a.td.text.replace(":", "_")).replace("[name]", desc))
        img.crop((x, y, x + 32, y + 32)).save(final)
        li[a.td.text] = 0
