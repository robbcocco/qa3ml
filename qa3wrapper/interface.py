import requests


def _url(question):
    return 'http://swipe.unica.it/apps/qa3/?q=' + question


def get_json(question):
    r = requests.get(_url(question))
    if r.status_code != 200:
        # print(r.status_code)
        return None
    return r.json()
