import os
import ast
import requests
from datetime import datetime, timedelta
import logging, json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Logging Variables
logger = logging.getLogger()
logger.setLevel(logging.INFO)

SECRET_EMAIL = os.environ.get("SECRET_EMAIL") or "YOUR EMAIL"
SECRET_PASSWORD = os.environ.get("SECRET_PASSWORD") or "YOUR PASSWORD"

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL") or "YOUR SLACK WEBHOOK URL"
SLACK_CHANNEL_NAME = "#worldcup-2022"

SLACK_USERNAME = "robot"
SLACK_ICON_EMOJI = ":robot_face:"

# Sweepstake function that associated country with a person
def ss(key):
    sweepstake = {
        "Germany": "Diogo",
        "Poland": "Minh",
        "South Korea": "Didier",
        "Australia": "Sri",
        "France": "Jose",
        "Senegal": "Fabian",
        "Mexico": "James Simmons",
        "Nederlands": "James",
        "Tunisia": "Andrew",
        "Henrique": "Croatia",
        "Uruguay": "Cristi",
        "Brazil": "Rita",
        "Argentina": "Colin",
        "Canada": "Darren",
        "Ghana": "Chavi",
        "Ecuador": "Luqman",
        "Saudi Arabia": "Theodore",
        "Denmark": "Martin",
        "Morocco": "Juan",
        "England": "Jeroen",
        "Iran": "Meghan",
    }

    for k in sweepstake:
        sweepstake[k] = f"{k} (*{sweepstake[k]}*)"

    return sweepstake.get(key, key)

# Slack Message function
def send_msg_to_slack(SLACK_MSG):
    payload = {
        'text': SLACK_MSG,
        'channel': SLACK_CHANNEL_NAME,
        'icon_emoji': SLACK_ICON_EMOJI,
        'username': SLACK_USERNAME
    }

    print('Sending Message to Slack')
    
    req = Request(SLACK_WEBHOOK_URL, json.dumps(payload).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", payload['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
    return 0

response = requests.post('http://api.cup2022.ir/api/v1/user/login', 
                json={
                  "email": SECRET_EMAIL,
                  "password": SECRET_PASSWORD
                }
            )

if response.status_code == 200:
    class BearerAuth(requests.auth.AuthBase):
        def __init__(self, token):
            self.token = token
        def __call__(self, r):
            r.headers["authorization"] = "Bearer " + self.token
            r.headers["Content-Type"] = "application/json"
            return r

    response = requests.get('http://api.cup2022.ir/api/v1/match', auth=BearerAuth(ast.literal_eval(response.text)["data"]["token"]))

    results = ast.literal_eval(response.text)["data"]

    today = datetime.now()
    todaydate = today.strftime("%m/%d/%Y")

    tomorrow = today + timedelta(days=1)
    tomorrowdate = tomorrow.strftime("%m/%d/%Y")

    resultstoday = list()
    gamestomorrow = list()

    for result in results:
        if todaydate == result["local_date"].split(" ")[0]:
            home = ss(result['home_team_en'])
            if result["finished"] == "TRUE":
                resultstoday.append(f"{home}{(27-len(home))* ' '} {result['home_score']} - {result['away_score']} {ss(result['away_team_en'])}")
            else:
                resultstoday.append(f"{home}{(27-len(home))* ' '} - {ss(result['away_team_en'])}")
        
        elif tomorrowdate == result["local_date"].split(" ")[0]:
            home = ss(result['home_team_en'])
            gamestomorrow.append(f"{home}{(27-len(home))* ' '} - {ss(result['away_team_en'])}")

    results = ""
    if resultstoday:
        results += f"_RESULTS TODAY - {todaydate}_\n"
        for val in resultstoday:
            results += "\t\t" + val + "\n"
    else:
        results += f"_NO RESULTS TODAY - {todaydate}_\n"

    if gamestomorrow:
        results += f"\n\n_MATCHES TOMORROW - {tomorrowdate}_\n"
        for val in gamestomorrow:
            results += "\t\t" + val + "\n"
    else:
        results += f"_NO MATCHES TOMORROW - {tomorrowdate}_\n"
    results += "\n"

    send_msg_to_slack(results)

else:
    print("Error - Try again later")