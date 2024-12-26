import os, json, random, time as t
import requests as r

LocalPath = os.getcwd()
eventFilePath = LocalPath + "/events.json"
def get_configuration():
    """ Reads configuration from the propagator.config file.
        Returns dict of all the data defined."""
    readData = {}
    try:
        with open(LocalPath + "/propagator.config", 'r') as file:
            for line in file.readlines():
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
        print(e)
        return -1

def read_events():
    try:
        with open(eventFilePath, 'r') as file:
            events = json.load(file)
        return events
    except Exception as e:
        print(e)
        return -1

def StartPropagator(configuration, events):
    url = configuration["endpoint"]
    period = int(configuration["period"])
    amountOfEvents = len(events) - 1
    print(url, period)
    while True:
        eventToSend = random.randint(0, amountOfEvents)
        try:
            response = r.post(url, events[eventToSend])
            print(response, events[eventToSend])
            t.sleep(period)
        except Exception as e:
            print(e)

configData = get_configuration()
eventData = read_events()
if configData != -1 and eventData != -1:
    StartPropagator(configData, eventData)
else:
    print("Configuration file was not read")

