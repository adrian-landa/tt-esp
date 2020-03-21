SETTINGS_FILE = '/settings.json'
MQTT_SERVER = 'a1rg8ma55rz9fs-ats.iot.us-west-2.amazonaws.com'
MQTT_PORT = 8883
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"config"
client = None
SD_PREFIX = '/sd'

JSON_LABEL_ESSID = 'essid'
JSON_LABEL_PASS = 'password'
JSON_LABEL_CONTENT = 'content'
JSON_LABEL_AUTOSTART = 'auto_start'