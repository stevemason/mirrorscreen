# Copyright 2021 Steve Mason

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Process messages from MQTT broker to control Raspberry PI Touchscreen backlight on/off."""

import paho.mqtt.client as mqtt
import config
import ssl
from light import setlight, getlight
from time import sleep
import sys
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(handlers=[RotatingFileHandler('./mirrorscreen.log', maxBytes=100000, backupCount=3)],
                    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def on_connect(client, userdata, flags, rc):
    """Subscribe to 'set' topic on connect."""
    if rc == 0:
        logging.info("Connected")
    else:
        logging.warning("Connection issue - result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(config.topic_set)
    publish_status(client)  # update the status on connect


def on_message(client, userdata, msg):
    """Process incoming message from MQTT broker."""
    # The only valid options are 'ON' and 'OFF'
    message = msg.payload
    if message == b"ON":
        logging.info("Light on")
        setlight('ON')
    elif message == b"OFF":
        logging.info("Light off")
        setlight('OFF')
    publish_status(client)  # update the status to reflect change


def publish_status(client):
    """Publish the live status of the backlight."""
    client.publish(config.topic_get, payload=getlight())


client = mqtt.Client(config.client_id)
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(config.cert, tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(False)
client.username_pw_set(config.username, config.password)

# Keep trying to connect until it succeeds
attempt = 0
connection_retry_delay = 60
while True:
    try:
        client.connect(config.mqtt_host, config.mqtt_port, 60)
    except OSError:
        attempt += 1
        logging.warning("Connection attempt #{} failed (waiting {}s).".format(
            attempt, connection_retry_delay))
        sleep(connection_retry_delay)
        continue
    except ssl.CertificateError:
        logging.critical(
            "There is a problem with the SSL certificate. Exiting.")
        sys.exit(1)
    else:
        break

client.loop_forever()
