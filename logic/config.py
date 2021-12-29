import json


def get_environment_variables():
    with open(r'C:\Users\Ivana\PycharmProjects\TwitterSentimentAnalysis\env.json', 'r', encoding="utf-8") as content:
        env_var_value = json.load(content)
    return env_var_value
