import os
import requests
import base64
from django.core.files.base import ContentFile

from app.models import Message


def create_message(content, image=None):
    message = Message(content=content, image=image)
    message.save()

    key_var_name = 'IMAGE_SUBSCRIPTION_KEY'
    if key_var_name not in os.environ:
        raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
    subscription_key = os.environ[key_var_name]

    language_api_url = "https://canadacentral.api.cognitive.microsoft.com/vision/v2.0/analyze?visualFeatures=Tags&language=en"

    images = {"url": "https://" + os.environ["DOMAIN"] + "/" + message.image.url}

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(language_api_url, headers=headers, json=images)
    tags = response.json()
    if "tags" in tags:
        message.image_tags = ";".join([t["name"] for t in tags["tags"] if t["confidence"] > 0.5][:5])
        message.save()

    key_var_name = 'TEXT_ANALYTICS_SUBSCRIPTION_KEY'
    if key_var_name not in os.environ:
        raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
    subscription_key = os.environ[key_var_name]

    endpoint_var_name = 'TEXT_ANALYTICS_ENDPOINT'
    if endpoint_var_name not in os.environ:
        raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
    endpoint = os.environ[endpoint_var_name]

    language_api_url = endpoint + "/text/analytics/v2.1/languages"

    documents = {"documents": [
        {"id": "1", "text": message.content}
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

    tags = [tag for tag in key_phrases["documents"][0]["keyPhrases"] if tag.count(" ") < 2]
    message.tags = ";".join(tags)
    message.save()

    return message


def get_messages(language: str = "en"):
    messages = Message.objects.all().order_by("created_at")
    msgs = []

    key_var_name = 'TRANSLATE_ANALYTICS_SUBSCRIPTION_KEY'
    if key_var_name not in os.environ:
        raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
    subscription_key = os.environ[key_var_name]

    endpoint_var_name = 'TRANSLATE_ANALYTICS_ENDPOINT'
    if endpoint_var_name not in os.environ:
        raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
    endpoint = os.environ[endpoint_var_name]

    for msg in messages:
        if msg.language != language:
            translation_api_url = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from=" + msg.language + "&to=" + language
            text = [{'Text': msg.content}]
            headers = {"Ocp-Apim-Subscription-Key": subscription_key}
            response = requests.post(translation_api_url, headers=headers, json=text)
            translations = response.json()
            tmp_img = dict(id=msg.id, content=translations[0]["translations"][0]["text"], language=msg.language, tags=[t for t in msg.tags.split(";") if t])
            if msg.image:
                tmp_img["image"] = "https://" + os.environ["DOMAIN"] + "/" + msg.image.url
                tmp_img["image_tags"] = [t for t in msg.image_tags.split(";") if t]
            msgs.append(tmp_img)
        else:
            if msg.image:
                msg.image = "https://" + os.environ["DOMAIN"] + "/" + msg.image.url
                msg.image_tags = [t for t in msg.image_tags.split(";") if t]
            msg.tags = [t for t in msg.tags.split(";") if t]
            msgs.append(msg)
    return msgs

