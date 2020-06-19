import paho.mqtt.client as mqtt

_CLIENT_ID = 'DTRE'
_BROKER_ADDRESS = 'acme.aws.thinger.io'
_BROKER_PORT = 1883
_PASSWORD = 'dtredtredtredtre'


class Telemetry:
    _instance = None

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    # The callback for when the client receives a CONNACK response from the server.
    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("$SYS/#")

    # The callback for when a PUBLISH message is received from the server.
    @staticmethod
    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
