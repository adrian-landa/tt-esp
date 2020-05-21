"""
MicroPython driver for APA 102 using SPI bus.
Requires a SPI bus. Provides write methods so the device 
can be communicate with a strip of APA102 leds

Example usage on ESP32:
    import machine
    driver = apa102.APA102(machine.SPI(1),level = 50, strip_length = 40)
    driver.write_strip()    
"""

import time


class APA102:
    def __init__(self, spi, level, strip_length):
        self.spi = spi
        self.strip_length = strip_length
        self.level = level

    def write_strip(self, strip):
        level = self.__compute_level(self.level)
        self.__preamble()
        for led in strip:
            buffer = bytearray([level,led[0],led[1],led[2]])
            self.spi.write(buffer)
        self.__afterword()

    def clear(self):
        self.__preamble()
        level = self.__compute_level(0)
        blank = 0
        for _ in range(self.strip_length):
            self.spi.write(bytearray([level,blank,blank,blank]))
        self.__afterword()

    def __preamble(self):
        for _ in range(4):
            self.spi.write(b'\x00')

    def __afterword(self):
        for _ in range(4):
            self.spi.write(b'\xFF')

    def __compute_level(self, level):
        header = b'\xE0'
        scaled = bytes([int(level * 31/100)])
        result = header[0] | scaled[0]
        return result
