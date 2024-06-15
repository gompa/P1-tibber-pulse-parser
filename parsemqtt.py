# <P1-tibber-pulse-parser python service to translate P1 tibber pulse mqtt messages to homeassistant compatible mqtt messages >
# Copyright (C) 2024  Gompa

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import paho.mqtt.client as mqtt
import json
from dotenv import dotenv_values
from translationtable import obisToString

config = dotenv_values(f"{os.path.dirname(os.path.realpath(sys.argv[0]))}/.env")
# mqtt server
mqttserverurl = config["mqttserverurl"] or "localhost"
mqttserverport = int(config["mqttserverport"]) or 1883

# mqtt topics
mqttOrigin = config["mqttOrigin"] or "tibber"
# destination of parserd messages
newmqttTopic = config["newmqttTopic"] or "powermeter"

enabletranslate = config["enabletranslate"] or True


# parser
def parsejsonmessage(currentmessage):
    for item in currentmessage:
        for nesteditem in currentmessage[item]:
            # print(nesteditem, currentmessage[item][nesteditem])
            mqttc.publish(
                f"{newmqttTopic}/status/{nesteditem}",
                currentmessage[item][nesteditem],
                qos=1,
            )


def on_message(client, userdata, message):
    # userdata is the structure we choose to provide, here it's a dict
    currentmessage = ""
    # try to parse message as utf-8 string
    try:
        currentmessage = message.payload.decode("utf-8")
    except:
        pass
    try:
        currentmessage = json.loads(currentmessage)
        parsejsonmessage(currentmessage)
    except:
        pass
    if type(currentmessage) != dict:
        for line in currentmessage.split("\r\n"):
            if "/" in line:
                userdata["Metertype"] = line
            linesplit = line.split("(")
            lineSplitLen = len(linesplit)

            if lineSplitLen == 2:
                # split in on ( to create key,value if value split length is 2
                key, value = linesplit
                # clean up remaining bracket
                value = value.replace(")", "")
                # if value has * it indecates it has a denomination string
                valuesHasDomination = False
                if len(value.split("*")) > 1:
                    valuesHasDomination = True

                if valuesHasDomination:
                    # if kw in value remove Domination and multiply by 1000 to get watt value
                    if "kW" in value.split("*")[1]:
                        userdata[key] = int(float(value.split("*")[0]) * 1000)
                else:
                    # split on denomination and only use first element
                    userdata[key] = value.split("*")[0]

            elif lineSplitLen == 3:
                key, date, value = linesplit
                value = value.replace(")", "")
                date = date.replace(")", "")
                # if denomination is m3 assume is gas meter
                if value.split("*")[1] == "m3":
                    userdata[key] = float(value.split("*")[0])
                    userdata["last-gas-update"] = date
            elif lineSplitLen > 3:
                # parse powerloss log
                if linesplit[0] == "1-0:99.97.0":
                    userdata[linesplit[0].replace(")", "")] = linesplit[1].replace(
                        ")", ""
                    )
                    logdata = {}
                    itemcount = 0
                    currentlogitem = ""
                    for item in linesplit[3:]:
                        itemclean = item.replace(")", "")
                        if itemcount == 1:
                            logdata[currentlogitem] = int(itemclean.split("*")[0])
                            itemcount = 0
                        elif itemcount == 0:
                            currentlogitem = itemclean
                            itemcount += 1

                    userdata[linesplit[2].replace(")", "")] = json.dumps(logdata)
        for item in userdata:
            # when enable translate is true and item found in translation table use translated name
            if item in obisToString and enabletranslate:
                mqttc.publish(
                    f"{newmqttTopic}/{obisToString[item]}", userdata[item], qos=1
                )
            else:
                mqttc.publish(f"{newmqttTopic}/{item}", userdata[item], qos=1)


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe(mqttOrigin)


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.user_data_set({})
mqttc.connect(mqttserverurl, mqttserverport, 60)
mqttc.loop_forever()
