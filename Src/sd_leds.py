import os
import sdcard
import machine
import ubinascii
import apa102
import time

if __name__ == '__main__':
    spi_sd = machine.SPI(2)
    spi_sd.init(sck=machine.Pin(18), mosi=machine.Pin(23), miso=machine.Pin(19))
    spi_apa = machine.SPI(1)
    spi_apa.init(baudrate = 8000000,sck=machine.Pin(14), mosi=machine.Pin(13), miso=machine.Pin(12))
    strip = apa102.APA102(spi_apa,10, 280)
    cs = machine.Pin(5, machine.Pin.OUT)
    sd = sdcard.SDCard(spi_sd, cs)
    vfs = os.VfsFat(sd)
    os.mount(vfs, '/sd')
    tmpFile = open('/sd/Test5.bin','r')
    for raw in tmpFile :
        line = raw.rstrip('\r\n')
        values = line.split(',')
        bytes_lines = list(map(lambda value: ubinascii.unhexlify(value),values))
        strip.write_strip(bytes_lines)
        time.sleep(0.1)
    tmpFile.close()
