import json


def get_environment_variables():
    with open(r'C:\Users\Ivan\PycharmProjects\twitterSentimentAnalysis\env.json', 'r') as content:
        env_var_value = json.load(content)
    return env_var_value
