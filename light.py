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

"""Get and Set Raspberry Pi backlight status."""

import config


def getlight():
    """Get state of backlight."""
    with open(lightpath, 'r') as light:
        lightstate = light.read(1)
        if lightstate == '0':
            return "ON"
        elif lightstate == '1':
            return "OFF"


def setlight(state):
    """Set state of backlight."""
    # Ensure that user that script is running under has write access to lightpath,
    # otherwise the script will fail.
    with open(lightpath, 'w') as light:
        if state == 'ON':
            light.write('0')
        elif state == 'OFF':
            light.write('1')


# For test/dev purposes were a physical backlight may not be available,
# preserve state in a local file instead.
if config.test == True:
    lightpath = "./bl_power"  # Use local file for test/dev
else:
    lightpath = "/sys/class/backlight/rpi_backlight/bl_power"
