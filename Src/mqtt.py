from umqtt.simple import MQTTClient
import ubinascii
import machine
import network
import time

MQTT_SERVER = "192.168.100.98"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"content"


def configure_station_point(essid, password):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    if sta.isconnected():
        sta.disconnect()
    sta.connect(essid, password)
    tries = 0
    while sta.status() == network.STAT_CONNECTING:
        if tries > 30:
            sta.active(False)
            break
        tries += 1
        time.sleep(1)
    return sta.isconnected()


def subscription_callback(topic, msg):
    print((topic, msg))


if __name__ == '__main__':
    configure_station_point('Totalplay-CD9A', 'CD9A427F7Gs6675y')
    client = MQTTClient(CLIENT_ID, MQTT_SERVER)
    client.set_callback(subscription_callback)
    client.connect()
    client.subscribe(TOPIC)
    try:
        while True:
            client.wait_msg()
    finally:
        client.disconnect()
