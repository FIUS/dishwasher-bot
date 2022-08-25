# dishwasher-bot

[![build](https://github.com/FIUS/dishwasher-bot/actions/workflows/buildMaster.yml/badge.svg)](https://github.com/FIUS/dishwasher-bot/actions/workflows/buildMaster.yml)
[![docker](https://img.shields.io/docker/v/fius/dishwasher-bot?label=docker)](https://hub.docker.com/r/fius/dishwasher-bot)

Matrix bot for our dishwasher sign

## Configuration

This software is configured by the following environment variables.

| Variable                                 | Default/Required | Description                                            |
| ---------------------------------------- | ---------------- | ------------------------------------------------------ |
| DISHWASHER_BOT_MATRIX_HOMESERVER         | required         | The URL of the matrix homeserver                       |
| DISHWASHER_BOT_MATRIX_USER               | required         | The user for the matrix homeserver                     |
| DISHWASHER_BOT_MATRIX_ACCESS_TOKEN       | required         | The access token for the matrix homeserver             |
| DISHWASHER_BOT_MATRIX_SESSION_FILE       | `session.txt`    | The filepath for the session file for matrix           |
| DISHWASHER_BOT_MQTT_CLIENT_ID            | required         | The client id for the mqtt client                      |
| DISHWASHER_BOT_MQTT_USER                 | required         | The user for the mqtt broker                           |
| DISHWASHER_BOT_MQTT_PW                   | required         | The password for the mqtt broker                       |
| DISHWASHER_BOT_MQTT_BROKER               | required         | The hostname/ip of the mqtt broker                     |
| DISHWASHER_BOT_MQTT_PORT                 | `1883`           | The port of the mqtt broker                            |
| DISHWASHER_BOT_MQTT_TOPIC_PREFIX         | required         | The topic prefix for the topics the bot publishes on   |
| DISHWASHER_BOT_MATRIX_AUTHORIZATION_ROOM | required         | The room, whoose members are authorized to use the bot |
| DISHWASHER_BOT_LOGLEVEL                  | `INFO`           | The loglevel of this bot                               |
