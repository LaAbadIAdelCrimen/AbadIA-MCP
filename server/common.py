import requests
from server.config import ABADIA_SERVER_URL
from server.logger_config import log

session_id = None

def sendCmd(url, command, type="json", mode="GET"):
    global session_id
    cmd = "{}/{}"
    headers = {}

    if session_id:
        headers['X-Session-Id'] = session_id
        log.info(f"Using session ID: {session_id}")

    if type == "json":
        headers['accept'] = 'application/json'
    else:
        headers['accept'] = 'text/x.abadIA+plain'

    try:
        if mode == "GET":
            r = requests.get(cmd.format(url, command), headers=headers)
        if mode == "POST":
            r = requests.post(cmd.format(url, command), headers=headers)
        
        # Log response status and snippet of body
        log.info(f"cmd ---> {cmd.format(url, command)} {mode} {r.status_code}")
        
    except requests.exceptions.RequestException as e:
        log.error(f"Vigasoco comm error: {e}")
        return None

    if type == "json":
        try:
            tmp = r.json()
            if r.status_code == 599:
                tmp['haFracasado'] = True
            return tmp
        except ValueError:
            log.error("Failed to decode JSON from response")
            return None
    else:
        return r.text
