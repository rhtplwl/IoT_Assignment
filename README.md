# IoT_Assignment
Python script for simulating sensors that can be used in a factory using MQTT protocol and send alert mail if subscriber reciever sensor value out of range. 

Files :

1. config.json : This file contain all the configuration information related to mqtt broker and the sensor details. We can also add more sensors if needed.
2. mainFile.py : This file has the main program in which we are taking the information from the file config.json.
3. mail.py : This file has the send_alert function which send the mail to the reciever if subscriber get the out of range sensor value.

Before running the code, put the valid credentials in config.json file for successfully sending the mail.

Usage
Running : python3 mainFile.py config.json



