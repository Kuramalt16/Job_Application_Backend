import os, json, random, time as t
import requests as r

LocalPath = os.getcwd()
eventFilePath = LocalPath + "/events.json"
def get_configuration(file_name):
    """ Reads configuration from the propagator.config file.
        Returns dict of all the data defined."""
    readData = {}
    try:
        with open(LocalPath + "/" + file_name, 'r') as file:
            for line in file.readlines():
                line = line.strip()
                if "#" in line or line.strip() == "": # filter out empty lines and comments
                    continue
                if '=' in line:
                    configuration = line.split("=")[0]
                    value = line.split("=")[1]
                    readData[configuration] = value
                else:
                    print("Error in configuration file, = was not found in line: ", list(line))
                    return -1
        return readData
    except Exception as e:
        print("Error occurred in opening the configuration file: ", e)
        return -1

def read_events():
    try:
        with open(eventFilePath, 'r') as file:
            events = json.load(file)
        if isinstance(events, list):
            return events
        else:
            raise Exception("data inside the event file is not a list format")
    except Exception as e:
        print(e)
        return -1

def StartPropagator(propagatorConfig, events, consumerConfig):
    url = "http://" + consumerConfig["host"] + ":" + consumerConfig["port"] + propagatorConfig["endpoint"]
    period = int(propagatorConfig["period"])

    amountOfEvents = len(events) - 1

    while True:
        eventToSend = random.randint(0, amountOfEvents)
        try:
            response = r.post(url, json=events[eventToSend])
            print("Response: ", response, events[eventToSend])  # for debugging
        except Exception as e:
            print(f"Connection could not be made, wait for {period} seconds and retry")
        t.sleep(period)

propagatorData = get_configuration("propagator.config")
eventData = read_events()
consumerData = get_configuration("consumer.config")
if -1 not in [propagatorData, eventData, consumerData]:
    StartPropagator(propagatorData, eventData, consumerData)
else:
    print("Configuration file was not read")

