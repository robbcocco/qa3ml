import requests

QA3 = 'QA3'
TAGME = 'TagMe'
TAGMETOKEN = '61b9d2a7-96f7-47e5-94ba-adc8539dc2fa-843339462'


def _url(question, site):
    if site is QA3:
        return 'http://swipe.unica.it/apps/qa3/?q=' + question
    elif site is TAGME:
        return 'https://tagme.d4science.org/tagme/tag?lang=en&epsilon=0.5&gcube-token='+TAGMETOKEN+'&text=' + question


def get_json(question, site='QA3'):
    r = requests.get(_url(question, site))
    if r.status_code != 200:
        # print(r.status_code)
        return None
    return r.json()
