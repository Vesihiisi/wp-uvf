#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('url', action="store")

url = parser.parse_args().url

template = "==Källor==" + '\n' + "*{{UVF|" + url.split("-")[-1] + " }}" + '\n' + "{{Auktoritetsdata" + "}}"


page = requests.get(url).content

def getMonthName(number):
    months = ["januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"]
    number = int(number)-1
    return months[number]

def replacePlace(string):
    places = {"Hfrs" : "Helsingfors", "Tfrs" : "Tammerfors"}
    if string in places:
        return places[string]
    else:
        return string

dead = False
categories = []

article = BeautifulSoup(page, 'html.parser').findAll("div", { "class" : "article" })[0].find("td").text
first_line = article.split(")")[0] + ")"
rest = ")".join(article.split(")")[1:])
lastname = first_line.split(", ")[0].strip()
firstname = first_line.split(", ")[1].split("(")[0].strip()

fullname = "'''" + firstname + " " + lastname + "'''"
born_vars = first_line.split("(")[1][:-1].split(" ")

if "d." in born_vars:
    dead = True


print(first_line)
born_day = born_vars[1].split("/")[0]
born_month = getMonthName(born_vars[1].split("/")[1])
born_year = born_vars[2]
born_place = replacePlace(born_vars[3])
categories.append("Födda " + born_year)
categories.append("Personer från " + born_place)

born_string = 'född [[{} {}]] [[{}]] i [[{}]]'.format(born_day, born_month, born_year, born_place)

if dead == True:
    if "där" in born_vars:
        # if born and dead at same place, shift the indices
        dead_day = born_vars[6].split("/")[0]
        dead_month = getMonthName(born_vars[6].split("/")[1])
        dead_year = born_vars[7]
        dead_string = 'död där [[{} {}]] [[{}]]'.format(dead_day, dead_month, dead_year)
    else:
        dead_day = born_vars[5].split("/")[0]
        dead_month = getMonthName(born_vars[5].split("/")[1])
        dead_year = born_vars[6]
        dead_place = replacePlace(born_vars[7])
        dead_string = 'död [[{} {}]] [[{}]] i [[{}]]'.format(dead_day, dead_month, dead_year, dead_place)
    categories.append("Avlidna " + dead_year)
else: #still alive
    dead_string = ""
    categories.append("Levande personer")

if "professors titel" in rest:
    categories.append("Finländska innehavare av professors namn")

string = '{}, {}, {}'.format(fullname, born_string, dead_string)

for i in range(len(categories)):
    categories[i] = "[[Kategori:" + categories[i] + "]]"

categories_string = '\n'.join(categories)
defaultsort = "{{STANDARDSORTERING:" + "}}"

with open(lastname + ".txt", 'w') as out:
    out.write(string + '\n\n' + rest + template + '\n' + defaultsort + '\n' + categories_string + "\n–")
