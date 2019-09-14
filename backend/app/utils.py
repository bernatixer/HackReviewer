import os

import requests

from app.models import Message


def create_message(title, content):
    message = Message(title=title, content=content)
    message.save()

    key_var_name = 'TEXT_ANALYTICS_SUBSCRIPTION_KEY'
    if not key_var_name in os.environ:
        raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
    subscription_key = os.environ[key_var_name]

    endpoint_var_name = 'TEXT_ANALYTICS_ENDPOINT'
    if not endpoint_var_name in os.environ:
        raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
    endpoint = os.environ[endpoint_var_name]

    language_api_url = endpoint + "/text/analytics/v2.1/languages"

    documents = {"documents": [
        {"id": "2", "text": message.content}
    ]}

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(language_api_url, headers=headers, json=documents)
    languages = response.json()

    message.language = languages["documents"][0]["detectedLanguages"][0]["iso6391Name"]
    message.save()

    keyphrase_url = endpoint + "/text/analytics/v2.1/keyphrases"

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(keyphrase_url, headers=headers, json=documents)
    key_phrases = response.json()

    message.tags = ";".join(key_phrases["documents"][0]["keyPhrases"])
    message.save()

    return message
