import urllib.request as request
import urllib.parse as parse
import json

DONTPAD_BASE_URL = "http://dontpad.com/"
DTRE_URL = 'dtre_scenarios'


def write(page, content):
    url = DONTPAD_BASE_URL + page
    data = parse.urlencode({"text": content})
    data = data.encode("utf-8")
    req = request.Request(url, data)
    with request.urlopen(req) as response:
        timestamp = response.read()
    return timestamp


def read_raw(page):
    with request.urlopen(DONTPAD_BASE_URL + page + ".body.json?lastUpdate=0") as response:
        resp = response.read()
    return resp


def read(page, full_json=False):
    content = json.loads(read_raw(page).decode())
    if "body" in content:
        return content["body"] if not full_json else content
    return ""


if __name__ == "__main__":
    print(read('shiforits'))
