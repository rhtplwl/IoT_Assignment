#import required modules
import sys
import json
import time
import random
import paho.mqtt.client as mqtt
from mail import send_alert

#callbacks definations

#Callback on connection to the broker and to subscribe
def on_connect(client, userdata, flags, rc):
    print("Connected with rc :" + str(rc))
    client.subscribe(topic)

#Callback to retrieve the msg from broker
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    sensor_type = payload.get("type")
    min_value, max_value = payload.get("range")
    value = payload.get("value")
    print("Data recieved : " + str(msg.payload))
    if value not in range(min_value, max_value):
        print("Value of "+ sensor_type + " is out of range. Value : " + str(value))
        send_alert(sender, receiver, login_pass, smtpserver, smtpport)


#Importing Data from the config.json file.
with open(sys.argv[1]) as handle:
    config = json.load(handle)
    mqtt_config = config.get("mqtt", {})
    mail_config = config.get("mail", {})
    misc_config = config.get("misc", {})
    sensors = config.get("sensors")

    interval = misc_config.get("interval_secs", 500)
    verbose = misc_config.get("verbose", False)

    if not sensors:
        print("No sensors specified.")
        exit()

    host = mqtt_config.get("host")
    port = mqtt_config.get("port")
    username = mqtt_config.get("username")
    password = mqtt_config.get("password")
    topic = mqtt_config.get("topic")

    sender = mail_config.get("sendermail")
    receiver = mail_config.get("receivermail")
    login_pass = mail_config.get("password")
    smtpserver = mail_config.get("smtpserver")
    smtpport = mail_config.get("port")


client = mqtt.Client() #Client object
print("Connecting : ")
client.username_pw_set(username, password) #authentication
client.connect(host, port) #connecting to the broker


keys = list(sensors.keys())

client.loop_start()
while True:
    sensor_id = random.choice(keys)
    sensor = sensors[sensor_id]
    min_val, max_val = sensor.get("range")
    val = random.randint(min_val, max_val)

    data = {
        "id": sensor_id,
        "value": val
    }

    for key in ["unit", "type","range","description"]:  
        value = sensor.get(key)

        if value is not None:
            data[key] = value


    payload = json.dumps(data)
    client.on_connect = on_connect
    client.on_message = on_message
    time.sleep(interval)
    client.publish(topic, payload)
    time.sleep(interval)

client.disconnect()
client.loop_stop()

