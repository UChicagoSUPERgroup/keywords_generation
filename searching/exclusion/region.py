from bs4 import BeautifulSoup
import urllib.request
import re

url = "http://www.geonames.org/advanced-search.html?q=&featureClass=A&startRow=0&maxRows=500"

country = []


def get_all(url):
    geonames = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(geonames, "lxml")
    soup = soup.find("div", id="search")
    countries = soup.find_all("table", class_="restable")
    table = countries[1].find_all("tr")

    for rows in table:
        try:
            td = rows.find_all("td")[2]
        except IndexError:
            continue
        if td is None:
            continue
        country.append(td.getText())
    link = soup.find_all('a', href=True)
    link = "http://www.geonames.org/" + link[-1]["href"] + "&maxRows=500"
    print(link)
    return link


def is_english(word):
    eng = re.findall(r"[a-zA-Z ]", word)
    if len(word) == len(eng):
        return True
    else:
        return False


#get_all(get_all(get_all(get_all(get_all(url)))))

# countries = []
# for x in country:
#     x = x.split(", ")
#     ls = [m for m in x if m != " " and m != ""]
#     countries += ls
#
# countries = list(set(countries))
# countries = [country for country in countries if is_english(country)]
# countries = ", ".join(countries)
#
# with open("countries.txt", "w") as f:
#     f.write(countries)
