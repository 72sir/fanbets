# coding: utf-8
import time

from django.http import HttpResponse
from django.shortcuts import render

URL = 'http://betting.gg11.bet/api/sportmatch/GetMostPopular?sportID=2357'
ALL_GAME = 'http://betting.gg11.bet/api/sportmatch/Get?sportID=2357'

# Create your views here.


def index(request):
    html = json_data_parser_html(URL)
    args = {
        "html": html,
        "bar": "/",
    }
    return render(request, 'index.html', args)


def all_game(request):
    html = json_data_parser_html(ALL_GAME)
    args = {
        "html": html,
        "bar": "all_game",
    }
    return render(request, 'index.html', args)


def json_index_body(request):
    html = json_data_parser_html(URL)
    return HttpResponse(html)


def json_all_game_html(request):
    html = json_data_parser_html(ALL_GAME)
    return HttpResponse(html)


def statistica(request):
    html = "<h1>Статистика еще в разработке.</h1>"
    args = {
        "html": html,
        "bar": "statistica",
    }
    return render(request, 'index.html', args)


def json_data_parser_html(url):
    # Функция парсит данные json и возвращает таблицу с результатом
    all_game_json = parse_courses(url)
    category_game = parse_game(all_game_json)

    tournament_game = category_game["tournament_game"]
    category_game = category_game["list_game"]

    html = ""
    for category in category_game:
        html += "<h1>" + category + "</h1><br>"
        for tournamet in tournament_game:
            cat_bool = True
            for product in all_game_json:
                if product["Category"] == category and product["Tournament"] == tournamet:
                    if cat_bool:
                        html += "<p style='font-size: 20px;'>" + tournamet + "</p><table class='table table-striped table-hover'><thead><tr><th> </th><th> </th>" \
                                "<th> </th><th> </th><th> </th><th> </th></tr></thead><tbody>"
                        cat_bool=False

                    html += "<tr style='font-size: 18px'><td style='width: 125px;'><span style='color:black'> " + str(
                            product["Date"]) + " </span>" \
                            "<b>" + str(product["MonthNameShort"]) + "</b> <u>" + str(
                            product["Time"]) + " </u></td><td style='width: 64px; text-align: center;'>" \
                            "<a href='" + str(product["StreamUrl"]) + "' target='_blank'> Video </a> </td><td style='text-align: center;'>"

                    if product["HomeTeamLogo"]:
                        html += "<a href='" + str(
                            product["HomeTeamLogo"]) + "' target='_blank'><img style='height: 30px;' src='" \
                                                       "" + str(product["HomeTeamLogo"]) + "' alt='blog post'></a>"

                    html += "<span class='red'> " + str(
                        product["Title_0"]) + "</span><span class='blue'> VS </span><span class='red'>" + str(
                        product["Title_1"]) + "</span> "

                    if product["OriginalAwayTeamLogo"]:
                        html += "<a href='" + product[
                            "OriginalAwayTeamLogo"] + "' target='_blank'><img style='height: 30px;' " \
                                                      "src='" + product["OriginalAwayTeamLogo"] + "' alt='blog post'></a>"

                    html += "</td><td class='fz_21' style='min-width: 60px; width: 60px;'>" + str(product["Value_0"]) + \
                            "</td><td class='fz_21' style='min-width: 60px; width: 60px;'>" + str(
                            product["Value_1"]) + "</td><td style='width: 100px;'><a class='btn btn-primary btn-sm btn-block' " \
                            "href='http://betting.gg11.bet/#/sport/match/" + str(product["MatchID"]) + "'>+ " + str(
                            product["MarketsCount"]) + "</a></td></tr>"
            html += "</tbody></table>"
    return html


def parse_game(arr_game):
    list_game = []
    catergory_game = []
    tournament_game = []

    for catergory in arr_game:
        bool_category = True
        for game in catergory_game:
            if catergory["Category"] == game:
                bool_category = False
        if bool_category:
            catergory_game.append(catergory["Category"])

    for tournament in arr_game:
        bool_category = True
        for game in tournament_game:
            if tournament["Tournament"] == game:
                bool_category = False
        if bool_category:
            tournament_game.append(tournament["Tournament"])

    # search game in all information game arr
    for game in catergory_game:
        bool_game = True
        for elem in arr_game:
            if elem["Category"] == game and bool_game:
                list_game.append(game)
                bool_game = False
    args = {
        "list_game": list_game,
        "tournament_game": tournament_game
    }

    return args


def parse_courses(url):
    import json
    import urllib2

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
