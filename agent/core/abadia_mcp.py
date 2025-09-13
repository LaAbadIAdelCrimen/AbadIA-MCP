import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ABADIA_SERVER_URL = os.getenv("ABADIA_SERVER_URL")
if not ABADIA_SERVER_URL:
    raise ValueError("ABADIA_SERVER_URL environment variable is not set.")

location_paths = {
    "library": "UP:UP:LEFT:UP",
    "church": "RIGHT:RIGHT:UP",
    "cell": "DOWN:DOWN:LEFT"
}

character_locations = {
    "abbot": "church",
    "jorge": "library"
}

def sendCmd(url, command, type="json", mode="GET"):
        cmd = "{}/{}".format(url, command)
        try:
            if (type == "json"):
                headers = {'accept': 'application/json'}
            else:
                headers = {'accept': 'text/x.abadIA+plain'}

            if mode == "GET":
                r = requests.get(cmd)
            if mode == "POST":
                r = requests.post(cmd)
            logging.info(f"cmd ---> {cmd} {r.status_code}")
        except:
            logging.error(f"Vigasoco comm error {r.status_code}")
            return None
        headers = {'accept': 'text/x.abadIA+plain'}

        cmdDump = "{}/abadIA/game/current".format(url)
        core = requests.get(cmdDump, headers=headers)

        headers = {'accept': 'application/json'}
        cmdDump = "{}/abadIA/game/current".format(url)
        r = requests.get(cmdDump, headers= headers)

        if (type == "json"):
            tmp = r.json()

            if r.status_code == 599:
                tmp['haFracasado'] = True
            return tmp
        else:
            return r.text