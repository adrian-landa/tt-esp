import network
import time
from microWebSrv import MicroWebSrv


def configure_access_point():
    ap = network.WLAN(network.AP_IF)  # create access point interface
    ap.active(True)  # activate the interface
    ap.config(essid='ESP_TT', password='Temporal123.')
    ap.config(authmode=3, dhcp_hostname='TTConfig')
    ap.ifconfig()


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


def get_networks_names():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    networks = sta.scan()
    sta.active(False)
    result = ""
    for net in networks:
        result = result + 'ssid:{0} level:{1}\n'.format(net[0].decode('ascii'), net[3])
    return result


@MicroWebSrv.route('/config')
@MicroWebSrv.route('/config/<error>')
def handler_config_get(client, response, args={}):
    file = open('www/config.html', 'r')
    content = file.read()
    file.close()
    response.WriteResponseOk(headers=None,
                             contentType='text/html',
                             contentCharset='UTF-8',
                             content=content)


@MicroWebSrv.route('/config', 'POST')
def handler_config_post(client, response):
    form = client.ReadRequestPostedFormData()
    essid = form['fieldESSID']
    password = form['fieldPassword']
    is_correct = configure_station_point(essid, password)
    if is_correct:
        file = open('www/done.html', 'r')
        content = file.read()
        file.close()
        response.WriteResponseOk(headers=None,
                                 contentType="text/html",
                                 contentCharset="UTF-8",
                                 content=content)
    else:
        response.WriteResponseRedirect('/config/error')


if __name__ == "__main__":
    configure_station_point()
    configure_access_point()
    uServer = MicroWebSrv(port=80, bindIP='0.0.0.0', webPath="/www/")
    uServer.Start(threaded=True)
