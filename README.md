# Worldcup 2022 Sweepstake Slack bot

The goal of this project is to send a daily update through Slack about Worldcup 2022 fixtures. It adds the names of the team members that have a particular team as per Sweepstake, so it promotes team engagement.

ADD NICE LOGO

## Getting Started

1. Create a new conda environment

```
conda create -n slackbot
conda activate slackbot
```

2. Install necessary packages

```
conda install poetry
poetry install
```

3. Register your email + password using https://github.com/raminmr/free-api-worldcup2022

This is the command you should run, where YOUR_NAME, YOUR_EMAIL and YOUR_PASSWORD should be udpated.
```
curl --location --request POST 'http://api.cup2022.ir/api/v1/user' \
--header 'Content-Type: application/json' \
--data-raw '{
"name" : "YOUR_NAME",
"email": "YOUR_EMAIL",
"password": "YOUR_PASSWORD",
"passwordConfirm" : "YOUR_PASSWORD"
}'
```

4. Export those environment variables locally using:
```
SECRET_EMAIL="YOUR_NAME"
SECRET_PASSWORD="YOUR_PASSWORD"
```

5. In the code, on the file [/worldcup2022-slackbot.py](/worldcup2022-slackbot.py) modify the `sweepstake` dictionary into the one that makes sense to your team. This is the free one I found and used for our team, and used it live: https://spinnerwheel.com/fifa-world-cup-sweepstake-generator.

6. Create a slack bot with incoming webhooks

* Go into https://api.slack.com/messaging/webhooks
* Create slack app
* Enable Incoming Webhooks
* Create an Incoming Webhook
* Select channel you are interested to use bot in, e.g. "#worldcup-2022"
* Grab the WebHook URL as seen below

<img width="647" alt="Screenshot 2022-11-24 at 01 01 15" src="https://user-images.githubusercontent.com/25267873/203671393-bcb76402-af8c-4343-b1a5-f41d22aae6a8.png">

7. Create an environment variable for your slack webhook url

```
export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

8. Run the app locally to test that you receive a slack bot message in the group
```
poetry run python worldcup2022-slackbot.py
```

output image

## Deploy

If you are happy with the previous outcome, you can deploy it using GitHub actions directly.

* Go into GitHub Settings -> Secrets -> Actions
* Create New Repository secret for SECRET_EMAIL, SECRET_PASSWORD and SLACK_WEBHOOK_URL

That should be it.

If you want to change the daily update time you should go into [/.github/workflows/worldcup2022_sweepstake_slackbot_daily_update.yml](/.github/workflows/worldcup2022_sweepstake_slackbot_daily_update.yml) and update the cron job accordingly.

## Happy tournament and let's go 🇵🇹

