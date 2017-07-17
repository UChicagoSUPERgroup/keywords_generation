from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd

url = "http://www.geonames.org/advanced-search.html?q=&featureClass=A&startRow=0&maxRows=500"


def get_page(url):
    country = []
    geonames = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(geonames, "lxml")
    soup = soup.find("div", id="search")
    countries = soup.find_all("table", class_="restable")
    table = countries[1].find_all("tr")

    for rows in table:
        try:
            cur_name = rows.find_all("td")[1]
            cur_country = rows.find_all("td")[2]
            cur_feature = rows.find_all("td")[3]
        except IndexError:
            continue
        if cur_name is None or cur_country is None or cur_feature is None:
            continue
        cur_name = cur_name.find("a", href=True)
        if cur_name is None:
            cur_name = "None"
        else:
            cur_name = cur_name.getText()
        cur_country = cur_country.getText()
        cur_feature = cur_feature.getText()
        country.append([cur_name, cur_country, cur_feature])
    return country


def next_page(url):
    geonames = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(geonames, "lxml")
    soup = soup.find("div", id="search")
    link = soup.find_all('a', href=True)
    innerlink = link[-1]["href"]

    start_page = re.search(r"startRow=(.*?)$", innerlink)

    if start_page is None:
        return
    start_page = innerlink[start_page.start() + 9: start_page.end()]
    if int(start_page) > 5000:
        return

    link = "http://www.geonames.org" + innerlink + "&maxRows=500"
    return link


def get_all(nextpage):
    country = []

    while True:
        country += get_page(nextpage)
        print(country)

        nextpage = next_page(nextpage)
        if nextpage is None:
            break
    return country


# total = get_all(url)


def is_english(word):
    eng = re.findall(r"[a-zA-Z ,]", word)
    if len(word) == len(eng):
        return True
    else:
        return False


with open("featureclass", "r") as f:
    data = f.readlines()
data = [x.replace('\n', "") for x in data]

def to_csv(countries, outfile):
    countries = [country for country in countries if is_english(country[0]) and is_english(country[1])]
    new_countries = []
    name_list = []
    for i in range(0, len(countries)):
        cur_country = countries[i]
        if cur_country[0] in name_list:
            continue
        else:
            name_list.append(cur_country[0])
        last_term = cur_country[-1]
        for term in data:
            if term in last_term:
                nes = [cur_country[0], cur_country[1], term]
                new_countries.append(nes)
                break

    df = pd.DataFrame(new_countries, columns=["name", "country", "class"])
    df.to_csv(outfile)

def get_countries(url):
    country = []
    geonames = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(geonames, "lxml")
    soup = soup.find('div', id='search')
    soup = soup.find("select")
    items = soup.find_all("option")
    text = [x.getText() for x in items]
    with open("co.txt", 'w') as f:
        f.write(",".join(text))
get_countries("http://www.geonames.org/advanced-search.html?q=&country=&featureClass=A&continentCode=")