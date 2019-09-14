import os
import sdcard
import machine

if __name__ == '__main__':
    spi = machine.SPI(2)
    spi.init(sck=machine.Pin(18), mosi=machine.Pin(23), miso=machine.Pin(19))
    cs = machine.Pin(5, machine.Pin.OUT)
    sd = sdcard.SDCard(spi, cs)
    vfs = os.VfsFat(sd)
    os.mount(vfs, '/sd')
    print(os.listdir('/'))
