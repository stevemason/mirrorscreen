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

"""Update mirror light status via MQTT."""

import paho.mqtt.publish as publish
from light import getlight
import config
import ssl
from time import sleep
import sys
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(handlers=[RotatingFileHandler('./mirrorscreen_update.log', maxBytes=100000, backupCount=3)],
                    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
tls_config = {'ca_certs': config.cert, 'tls_version': ssl.PROTOCOL_TLSv1_2}
auth_config = {'username': config.username, 'password': config.password}

# If MQTT connection is unsuccessful,keep trying for a minute
light_status = getlight()
attempt = 0
connection_retry_delay = 10
while attempt < 6:
    try:
        publish.single(config.topic_get, payload=light_status, hostname=config.mqtt_host,
                       port=config.mqtt_port, client_id=config.update_client_id, auth=auth_config, tls=tls_config)
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
        logging.info("Light status: {}".format(light_status))
        break
