import sys
import json
import time
import random
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with rc :" + str(rc))
    client.subscribe(topics)

def on_message( client, userdata, msg):
    print(str(msg.payload))



with open(sys.argv[1]) as handle:
    config = json.load(handle)
    mqtt_config = config.get("mqtt", {})
    misc_config = config.get("misc", {})
    sensors = config.get("sensors")

    interval = misc_config.get("interval_secs", 500)
    verbose = misc_config.get("verbose", False)

    if not sensors:
        print("no sensors specified in config, nothing to do")
        exit()

    host = mqtt_config.get("host")
    port = mqtt_config.get("port")
    username = mqtt_config.get("username")
    password = mqtt_config.get("password")
    topic = mqtt_config.get("topic")

client = mqtt.Client()
client.on_connect = on_connect

# if username:
#     client.username_pw_set(username, password)

client.connect(host, port)
client.username_pw_set(username, password)

keys = list(sensors.keys())

while True:
    sensor_id = random.choice(keys)
    sensor = sensors[sensor_id]
    min_val, max_val = sensor.get("range", [0, 100])
    val = random.randint(min_val, max_val)

    data = {
        "id": sensor_id,
        "value": val
    }

    for key in ["unit", "type", "description"]:  
        value = sensor.get(key)

        if value is not None:
            data[key] = value

    payload = json.dumps(data)

    if verbose:
        print("%s: %s" % (topic, payload))

    client.publish(topic, payload)
    time.sleep(interval)


