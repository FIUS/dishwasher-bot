"""Main module of the dishwasher bot."""
from logging import Logger, lastResort
from os import environ

from paho.mqtt import client as mqtt_client
import simplematrixbotlib as botlib
from .commands import Commands
from . import Dishwasher, Action


def die(*args: object):
    """Exit with message."""
    raise SystemExit(args)


def load_from_env(name: str, default=None) -> str:
    """Load the given variable from the environment."""
    return environ.get(name) or default or die(f"Need the {name} in env")


logger = Logger(__name__)
QOS = 1
RETAIN = False


def main():
    """Run the bot."""
    global bot
    creds = botlib.Creds(
        homeserver=load_from_env("DISHWASHER_BOT_MATRIX_HOMESERVER"),
        username=load_from_env("DISHWASHER_BOT_MATRIX_USER"),
        login_token=load_from_env("DISHWASHER_BOT_MATRIX_LOGIN_TOKEN"),
        session_stored_file=load_from_env("DISHWASHER_BOT_MATRIX_SESSION_FILE", "./session.txt")
    )

    config = botlib.Config()
    config.encryption_enabled = True
    config.emoji_verify = False
    config.ignore_unverified_devices = True
    config.store_path = load_from_env("DISHWASHER_BOT_CRYPTO_STORE_PATH", "./crypto-store/")

    bot = botlib.Bot(creds, config)

    # Connect to mqtt
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
        else:
            logger.warning("Failed to connect to broker, return code %d\n", rc)
    client = mqtt_client.Client(load_from_env("DISHWASHER_BOT_MQTT_CLIENT_ID"))
    client.username_pw_set(load_from_env("DISHWASHER_BOT_MQTT_USER"), load_from_env("DISHWASHER_BOT_MQTT_PW"))
    client.on_connect = on_connect
    client.connect(
        load_from_env("DISHWASHER_BOT_MQTT_BROKER"),
        int(load_from_env("DISHWASHER_BOT_MQTT_PORT", "1883")),
        keepalive=10)
    client.loop_start()

    topic_prefix = load_from_env("DISHWASHER_BOT_MQTT_TOPIC_PREFIX")
    if not topic_prefix.endswith("/"):
        topic_prefix += '/'

    def send_action(dishwasher: Dishwasher, action: Action):
        logger.info("Sending action: %s for %s", action.value, dishwasher.value)
        topic = topic_prefix + dishwasher.value + '/' + action.value
        payload = f'{{"topic": "{topic}","dishwasher": "{dishwasher.value}","action": "{action.value}"}}'
        client.publish(topic, payload, qos=QOS, retain=RETAIN)

    Commands(bot, load_from_env("DISHWASHER_BOT_MATRIX_AUTHORIZATION_ROOM"), send_action)

    logger.info("Starting bot...")
    bot.run()


if __name__ == "__main__":
    LOGLEVEL = load_from_env('DISHWASHER_BOT_LOGLEVEL', 'INFO').upper()
    lastResort.setLevel(LOGLEVEL)
    main()
