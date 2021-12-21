import json


def get_environment_variables():
    with open(r'C:\Users\Ivan\PycharmProjects\twitterSentimentAnalysis\envVar.json', 'r') as content:
        env_var_value = json.load(content)
    return env_var_value
