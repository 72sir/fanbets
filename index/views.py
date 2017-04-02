# coding: utf-8
import urllib2
import json
import time

from django.shortcuts import render

URL = 'http://betting.gg11.bet/api/sportmatch/GetMostPopular?sportID=2357'
ALL_GAME = 'http://betting.gg11.bet/api/sportmatch/Get?sportID=2357'


# Create your views here.


def index(request, *args):
    # Проверяем передавались ли нам параметры
    # если нет то активируем переменную
    if args is None:
        args = {}

    args = parse_courses(URL)
    args = {"products": args, "bar": "/"}

    return render(request, 'index.html', args)


def all_game(request, *args):
    # Проверяем передавались ли нам параметры
    # если нет то активируем переменную
    if args is None:
        args = {}

    args = parse_courses(ALL_GAME)
    args = {"products": args, "bar": "all_game"}

    return render(request, 'index.html', args)


def parse_courses(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

    f = opener.open(url)
    f_read = f.read()

    i = 0
    list = []

    try:
        f_json = json.loads(f_read)

        while True:
            try:
                _str = str(f_json[i]["DateOfMatchLocalized"]["Date"])
                _str = _str[3:5]
                list.append({
                    "DateOfMatchLocalized": str(f_json[i]["DateOfMatchLocalized"]["Value"]),
                    "MonthNameShort": str(f_json[i]["DateOfMatchLocalized"]["MonthNameShort"]),
                    "Time": str(f_json[i]["DateOfMatchLocalized"]["Time"]),
                    "Date": _str,
                    "MarketsCount": f_json[i]["MarketsCount"],
                    "MatchID": f_json[i]["PreviewOdds"][0]["MatchID"],
                    "Title_0": f_json[i]["PreviewOdds"][0]["Title"],
                    "Title_1": f_json[i]["PreviewOdds"][1]["Title"],
                    "Value_0": f_json[i]["PreviewOdds"][0]["Value"],
                    "Value_1": f_json[i]["PreviewOdds"][1]["Value"],
                    "OriginalAwayTeamLogo": f_json[i]["OriginalAwayTeamLogo"],
                    "HomeTeamLogo": f_json[i]["HomeTeamLogo"],
                    "StreamUrl": f_json[i]["StreamUrl"],
                    "Tournament": f_json[i]["Tournament"]["Name"],
                    "Category": f_json[i]["Category"]["Name"],
                })
                i += 1
            except:
                break

    except ValueError:
        print("error json structure")

    return list





