import json


def get_env_variables():
    with open(r'C:\Users\Ivan\PycharmProjects\SCRAPING-StockTwitter\env.json', 'r', encoding="utf-8") as content:
        env_var_value = json.load(content)
    return env_var_value
