import json


def environment_variables():
    with open(r'C:\Users\Ivan\PycharmProjects\SCRAPING-StockTwitter\env.json', 'r', encoding="utf-8") as content:
        env_var = json.load(content)
    return env_var
