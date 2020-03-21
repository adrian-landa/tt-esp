from umqtt.simple import MQTTClient
import gc
import ubinascii
gc.collect()
import machine
gc.collect()
import network
import time
import usocket as socket
import os
import sdcard
import json

MQTT_SERVER = 'a1rg8ma55rz9fs-ats.iot.us-west-2.amazonaws.com'
MQTT_PORT = 8883
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"config"
client = None
SD_PREFIX = '/sd'


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

def configure_mqtt_client():
    global client
    certFile = open("/cert", "r")
    cert = certFile.read()
    certFile.close()
    keyFile = open("/privateKey", "r")
    key = keyFile.read()
    keyFile.close()
    client = MQTTClient(client_id=MQTT_CLIENT_ID, server=MQTT_SERVER,
                        port=MQTT_PORT, keepalive=5000, ssl=True,
                        ssl_params={"cert": cert, "key": key, "server_side": False})       
    client.set_callback(subscription_callback)
    client.connect()
    client.subscribe(TOPIC)
    print('Subscrito')


def mount_sd(prefix):
    spi = machine.SPI(2)
    spi.init(sck=machine.Pin(18), mosi=machine.Pin(23), miso=machine.Pin(19))
    cs = machine.Pin(5, machine.Pin.OUT)
    sd = sdcard.SDCard(spi, cs)
    vfs = os.VfsFat(sd)
    os.mount(vfs, prefix)
    return spi


def umount_sd(spi, prefix):
    os.umount(prefix)
    spi.deinit()


def download_file(host, path, port):
    spi_sd = mount_sd(SD_PREFIX)
    file_name = path.split('/')[-1]
    headers_limit = '\r\n\r\n'.encode('ascii')
    has_headers_ended = False
    request = 'GET {0} HTTP/1.0\r\nHost:{1}\r\n\r\n'.format(path, host)
    file = open(SD_PREFIX + '/' + file_name, 'wb')
    '''Sección de configuración de sockets'''
    socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_connection.connect((host, port))
    socket_connection.send(request.encode('ascii'))
    while True:
        data = socket_connection.recv(2048)
        if not data:
            break
        else:
            response = data.split(headers_limit)
            if len(response) > 1:
                has_headers_ended = True
            if has_headers_ended:
                print("Escribiendo")
                file.write(response[-1])
    file.close()
    socket_connection.close()
    print(os.listdir(SD_PREFIX))
    umount_sd(spi_sd, SD_PREFIX)


def subscription_callback(topic, msg):
    print((topic, msg))
    payload = json.loads(msg)
    path = payload['file']
    download_file('192.168.100.124', path, 8000)


configure_station_point('Totalplay-CD9A', '864LUP99r')
time.sleep(1)
configure_mqtt_client()
time.sleep(1)

try:
    while True:
        client.check_msg()
        time.sleep(0.3)
finally:
    client.disconnect()
