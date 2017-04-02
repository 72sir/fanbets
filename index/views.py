# coding: utf-8
import urllib2
import json

from django.shortcuts import render

URL = 'http://betting.gg11.bet/api/sportmatch/GetMostPopular?sportID=2357'
URL_GetLive = 'http://betting.gg11.bet/api/sportmatch/GetLive?isGetTop=true'


# Create your views here.


def index(request, *args):
    # Проверяем передавались ли нам параметры
    # если нет то активируем переменную
    if args is None:
        args = {}

    args = parse_courses()
    args = {"products": args}

    for prod in args["products"]:
        print(prod)

    return render(request, 'index.html', args)


def parse_courses():
    list = []

    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

    f = opener.open(URL)
    f_read = f.read()
    i = 0

    try:
        f_json = json.loads(f_read)

        while i < 10:
            _str = str(f_json[i]["DateOfMatchLocalized"]["Date"])
            _str = _str[:2]

            list.append({
                "DateOfMatchLocalized": str(f_json[i]["DateOfMatchLocalized"]["Value"]),
                "MonthNameShort": str(f_json[i]["DateOfMatchLocalized"]["MonthNameShort"]),
                "Date": _str,
                "MarketsCount": f_json[i]["MarketsCount"],
                "MatchID": f_json[i]["PreviewOdds"][0]["MatchID"],
                "Title_0": f_json[i]["PreviewOdds"][0]["Title"],
                "Title_1": f_json[i]["PreviewOdds"][1]["Title"],
                "Value_0": f_json[i]["PreviewOdds"][0]["Value"],
                "Value_1": f_json[i]["PreviewOdds"][1]["Value"],
                "OriginalAwayTeamLogo": f_json[i]["OriginalAwayTeamLogo"],
            })

            i += 1

    except ValueError:
        print("error json structure")

    return list