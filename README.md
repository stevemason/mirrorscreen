Mirrorscreen
============

This project contains a couple of scripts related to controlling the backlight of the official Raspberry Pi touchscreen using MQTT.

mirrorscreen.py
---------------

This script subscribes to MQTT topics to turn the backlight on/off, and immediately reports back the new backlight status.

mirrorscreen_update.py
----------------------

This script is used for one-off MQTT updates on the status of the backlight.

Implementation example
----------------------

I have a smart mirror (or magic mirror) powered by a Raspberry Pi, and I want to be able to turn off the backlight to save energy, as required. I have a separate MQTT broker set up to manage communications to/from the Raspberry Pi.

A cron job is set up to turn the light on in the morning and off in the evening. 'mirrorscreen_update.py' is used to report the status change back via the MQTT broker.

The backlight can also be controlled using the Home app on my IOS devices. The Home app talks to Homebridge, which in turn talks to the MQTT broker via the Homebridge Mqttthing plugin. 'mirrorscreen.py' is used to listen for instructions from the Home app, and turn the backlight on/off.
