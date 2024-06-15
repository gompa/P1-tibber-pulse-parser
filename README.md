

## P1 tibber Pulse parser



P1 Tibber Pulse parser is an MQTT client that parses and publishes the Pulse MQTT messages to a simple importable format in Home Assistant without sending the data to the cloud.


**to get started:**

1. setup the pulse
2. setup the parser
3. setup homeasistant 


## Setup Pulse

The first step to connect the **Pulse** to your own network is to force it into AP mode. By doing a hard reset, it will appear in the network as an access point.
Use a paper clip to reset the **Pulse**, it has a small hole for resetting to factory defaults. 
It is on the opposite side of where the micro-USB connector is.
To supply the **Pulse** with power use a mobile charger or similar.
When the power is connected, use an unfolded paper clip in the small hole and press until the **Pulse** begins to flash rapidly (after about 5 seconds). 
It should now be possible to find a wireless network with the SSID **Tibber Pulse**.
You can connect a PC or mobile phone to this network. The password is on the back of the **Pulse** in **bold** text in a frame. When the **Pulse** has accepted the connection, you can check what ipadress you get on your wireless interface for example : **10.133.70.2** to reach the pulse in your browser go to address **http://10.133.70.1**. the **Pulse's** webpage that appears will look like this:

![Pulse in AP mode](https://github.com/iotux/ElWiz/blob/master/Pulse-AP.jpg)

Populate the fields **ssid** and **psk** with the name of your own WiFi router and password.

Populate the fields **mqtt_url** and **mqtt_port** with the **IP address** of your own broker and port number **1883** for use without SSL. or **8883** for use with SSL.\
If the broker is set up to require authentication with username and password, enter them in the **mqtt_url** field.

If the username is **janedoe** and the password is **secret1**, then this is specified like this:

**janedoe:secret1@your.broker.address**,

where broker-address can be a **FQDN hostname** or **IP adress**.

the field **mqtt_topic** is a a freely chosen topic. It should be different from the topic used by the pulse to recieve messages to use the parser without chaning this field in the config use: **tibber** 

The **mqtt_topic_sub** field is a **topic** that the **Pulse** subscribes to. To indicate that **MQTT messages** go the opposite way, you can e.g. use **rebbit** here. This ensures that it does not conflict with other **MQTT messages**. So far iotux found that by sending the message _"reboot"_, **Pulse** will respond with _"Debug: rebooting"_ and reboot. If you e.g. sends the message _"nonsense"_, then it will respond with _"Debug: Unknown command 'nonsense'"_. There is more about this in the section **Controlling Pulse**.

The **update_url** field seems to need a value. I have used the address of my own broker here. The purpose is obviously for upgrading the firmware in **Pulse**.
It would be interesting to get information about this if anyone has.

The other fields can be left empty unless you want to use **SSL**. When the fields have been filled in and sent to **Pulse**, a few seconds pass and it starts flashing green. It is a sign that **Pulse** is connected to your own network. When that happens, it is no longer in **AP mode** and access to the web interface is no longer possible. Once this is done, simply plug the **Pulse** into the **P1 connector** of the **P1 meter** and the **Pulse** will start delivering MQTT messages.

## Setup Parser

first install the requirements:
```pip3 install -f requirements.txt```

To set up the parser, you need to change the values of the `.env` file to your values.\
The MQTT server and topic should be the same MQTT server as the Pulse connects to.\
Set the `newmqttTopic` value to where you want the parsed values to go.\
You can choose to disable the translation of OBIS keys to a human-readable format by setting `enabletranslate = False` (default is `True`).




test if it functions like expected by runing parsemqtt.py:\
```python3 parsemqtt.py```

an easy way to check if the values are parsed on the server connect to the server with [mqtt-explorer](https://mqtt-explorer.com/)

if everything functions as expected add a systemd service to start start it on boot:
```
[Unit]
Description=Mqtt parser
After=multi-user.target
[Service]
Type=simple
Restart=always
ExecStart=python3 /script-location/parsemqtt.py
[Install]
WantedBy=multi-user.target
```




## setup homeasisstant

To read out the "new" values, add the following to your Home Assistant config.

If you changed the topic `newmqttTopic` the parser publishes to, you will need to change that in your config too.


```
mqtt:
  sensor:
    - name: current-return
      unit_of_measurement: "W"
      state_class: measurement
      state_topic: "powermeter/Actual-electricity-power-to-grid-in-W"
    - name: current-consumption
      device_class: power
      unit_of_measurement: "W"
      state_class: measurement
      state_topic: "powermeter/Actual-electricity-power-from-grid-in-W"


    - name: used-tarrif1
      device_class: energy
      unit_of_measurement: "Wh"
      state_class: total_increasing
      state_topic: "powermeter/electricity-delivered-to-client-(Tariff-1)-in-Wh"
    - name: used-tarrif2
      device_class: energy
      unit_of_measurement: "Wh"
      state_class: total_increasing
      state_topic: "powermeter/electricity-delivered-to-client-(Tariff-2)-in-Wh"



    - name: deliverd-tarrif1
      device_class: energy
      unit_of_measurement: "Wh"
      state_class: total_increasing
      state_topic: "powermeter/electricity-delivered-by-client-(Tariff-1)-in-Wh"
    - name: deliverd-tarrif2
      device_class: energy
      unit_of_measurement: "Wh"
      state_class: total_increasing
      state_topic: "powermeter/electricity-delivered-by-client-(Tariff-2)-in-Wh"


    - name: used-gas
      device_class: gas
      unit_of_measurement: "m³"
      state_class: total
      state_topic: "powermeter/gas-delivered-to-client-in-m3"

```

now you can add the entities to the energy tab in homeassistant



## Control the Pulse

the **Pulse** has some features that can be controlled using **MQTT messages**. This is done by sending the messages with the **topic** specified in the **mqtt_topic_sub** field in the web interface. This is not documented, but by trying different options, iotux has found these functions.

- reboot - Restarts **Pulse**
- update - OTA update of driver software (information about "update_url" is missing)

Those who use the **mosquitto** broker have access to **mosquitto_pub** to publish opinions. By using the **mqtt_topic_sub** that was specified in the setup of **Pulse**, e.g. **rebbit**, then a command to **Pulse** will look like this when you send the message **reboot**:

```
mosquitto_pub -h localhost -t rebbit -m reboot
Debug: Reboot
```

By sending the **update** command, we saw this response:

```
mosquitto_pub -h localhost -t rebbit -m "update"
Debug: Update in progress
Debug: Firmware update failed: -1
```


## Notes

I've only tested the parser with a single-phase power meter with a gas meter attached.
I've implemented most OBIS messages, but I can't test what my meter doesn't supply
the P1 standard pdf is included in the doc dir so you can find the OBIS codes if something is missing


thanks iotux/ElWiz
for the original pulse setup guide


