# Devman Bot Lesson 3

This is study project for [lesson 3](https://dvmn.org/modules/chat-bots/lesson/support-bot/)
Simple AI for decrease burden on users' support department

### Demo

- [telegram bot](https://t.me/rkinwork_dvmn_support_bot)
- [vk bot](https://vk.com/im?sel=-187412453)

Send messages like:
- Хочу работать у вас
- Привет
- Разбаньте

for more questions look at `src/train.json` file.  

### Prerequisites

To start working with project you need to:

- Installed [Git](https://git-scm.com/)
- Installed [Docker Desktop](https://www.docker.com/)
- DialogFlow [Register](https://cloud.google.com/dialogflow/es/docs/quick/setup) and
  add [Agent](https://cloud.google.com/dialogflow/es/docs/quick/build-agent)
- Get Dialog flow project id and credentials
- [Register](https://telegram.me/BotFather) bot in telegram and get token
- Obtain token for your VK group (Optional)

### Installing

Clone project

```
git clone git@github.com:rkinwork/dvmn-support-bot.git
```

Create .env file and required environment variables from settings section to it.
Put create `credentials.json` in project root and put there google auth private key

Train you bot with script
```bash
make start_train
```

If you run this script once again it will end with error showing that you have already trained the model.
If you want to train once again you should login and delete intents manually.

## Run service

To start telegram bot working

```bash
make start_tg
```

To stop bot working input in another console

To start VK bot working

```bash
make start_vk
```

### Settings

| ENV variable                   | Description                          | Is Required? |
|--------------------------------|--------------------------------------|--------------|
| DVMN_BOT__DEBUG                | True or False to toggle debug mode   ||
| DVMN_BOT__DIALOG_FLOW_ID       | id of the DiologFlow project         | True         |
| DVMN_BOT__TELEGRAM_CREDS       | token of telegram bot                | True         |
| DVMN_BOT__VK_CREDS             | token from your VK group             | True         |
| DVMN_BOT__CHAT_ID              | telegram chat id of the admin user   | True         |
| GOOGLE_APPLICATION_CREDENTIALS | path to your google credentials JSON | True         |


## Authors

* **DVMN.ORG TEAM** - *Idea*
* **Roman Kazakov** - *Implementation*

## License

MIT License

Copyright (c) 2023 Roman Kazakov

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

