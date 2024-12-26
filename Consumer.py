from flask import Flask, request, jsonify
import sqlite3, os, json

LocalPath = os.getcwd()

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
        print("Error occured trying to read the configuration file: ", e)
        return -1


consumerConfigData = get_configuration("consumer.config")
propagatorConfigData = get_configuration("propagator.config")

app = Flask("Consumer")


def init_db():
    """Initialise sqlite database if table doesn't exist create a new one"""
    conn = sqlite3.connect(consumerConfigData["db_name"])
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            event_payload TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route(propagatorConfigData["endpoint"], methods=['POST'])
def consume_event():
    """Once a POST event has been sent to the endpoint try to get the data"""
    # Get payload
    try:
        event_data = request.get_json()
        if not event_data:
            return jsonify({"error": "Invalid data"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to parse data: {str(e)}"}), 400

    # Upload to db
    if len(list(event_data.keys())) == 2 and event_data.get("event_type") != None and event_data.get("event_payload") != None:
        """if event data is a dictionary that has only two keys: event_type and event_payload"""
        if isinstance(event_data["event_type"], str) and isinstance(event_data["event_payload"], str):
            """if event data values are both strings"""
            try:
                conn = sqlite3.connect(consumerConfigData["db_name"])
                cursor = conn.cursor()
                cursor.execute("INSERT INTO events (event_type, event_payload) VALUES (?, ?)",
                               (event_data["event_type"], json.dumps(event_data["event_payload"])))
                conn.commit()
                conn.close()
                return jsonify({"message": "Event saved successfully"}), 201
            except Exception as e:
                return jsonify({"error": f"Failed to save event: {str(e)}"}), 500
        else:
            return jsonify({"error": f"Data values do not match the required format"}), 501
    else:
        return jsonify({"error": f"Data keys do not match the required format"}), 502

if __name__ == '__main__':
    init_db()
    try:
        app.run(debug=True, host=consumerConfigData["host"], port=int(consumerConfigData["port"]))
    except Exception as e:
        print("Error occurred trying to run the app: ", e)