import os
import sdcard
import machine
import ubinascii
if __name__ == '__main__':
    spi = machine.SPI(2)
    spi.init(sck=machine.Pin(18), mosi=machine.Pin(23), miso=machine.Pin(19))
    cs = machine.Pin(5, machine.Pin.OUT)
    sd = sdcard.SDCard(spi, cs)
    vfs = os.VfsFat(sd)
    os.mount(vfs, '/sd')
    file = open('/sd/Test5.bin','r')
    line = file.readline().rstrip('\r\n')
    values = line.split(',')
    print(values)
    print(len(values))
    byte_line = list(map(lambda value: ubinascii.unhexlify(value),values))
    print(byte_line)
    file.close()
