#
# PyoT Intel Galileo Platform
#
# Michael Rosen
# mrrosen
# 09-10-2015
#

import mraa
import serial
from pyotlib.classes import *

# Function to make peripheral
def create(params):
  return GalileoPlatform(params);
  
class GalileoPlatform(peripheral.Peripheral):

  # The build method, should create all the ports/pins on the board
  def build(self, params):
    # Declare the pin tracker, note:
    #   0-13 : Digital Pins
    #  14-19 : Ain Pins
    #  20-21 : I2C Bus
    #  22    : USB port
    self.pins = pin.Pins(range(23));
    
    # Set up all the ports from the given pins
    for i in xrange(20):
      self.pins.assign(self.endpoints.add(("gpio%d" % i), GalileoPlatform.GPIO), [i]);
    #for i in xrange(14, 20):
    #  self.pins.assign(self.endpoints.add(("ain%d" % (i - 14)), GalileoPlatform.AIN), [i]);
    #self.pins.assign(self.endpoints.add("i2c1", GalileoPlatform.I2C), [20, 21]);
    self.pins.assign(self.endpoints.add("spi1", GalileoPlatform.SPI), [10, 11, 12, 13]);
    #self.pins.assign(self.endpoints.add("uart2", GalileoPlatform.UART), [22]);
    #self.pins.assign(self.endpoints.add("uart1", GalileoPlatform.UART), [0, 1]);
    
    return;
    
  # GPIO Class for Galileo (uses mraa to do everything)
  class GPIO(interface.GPIO):
      
    # Build function (time to create stuff)
    def build(self, params):
      self.__gpio = mraa.Gpio(self._pin);
      return;
      
    # Request function
    def request(self, params):
      if (not(self.pins.request(self))):
        return False;
    
      if ("mode" in params):
        if (params['mode'] == "PULLDOWN"):
          self.__gpio.mode(mraa.MODE_PULLDOWN);
        elif (params['mode'] == "PULLUP"):
          self.__gpio.mode(mraa.MODE_PULLUP);
          
          
      if (("dir" in params) and (params['dir'] == "OUT")):
        self.__gpio.dir(mraa.DIR_OUT);
      else:
        self.__gpio.dir(mraa.DIR_IN);
        
      return True;
    
    # GPIO functions    
    def write(self, val):
      self.__gpio.write(val);
      return;
      
    def read(self):
      return self.__gpio.read();
      
  # SPI Class for Galileo (uses mraa to do everything)
  class SPI(interface.SPI):
  
    # Build function, creates Spi object
    def build(self, params):
      self.__spi = mraa.Spi(1);
      return;
      
    # Request function
    def request(self, params):
      if (not(self.pins.request(self))):
        return False;
      
      if ("frequency" in params):
        self.__spi.frequency(params['frequency']);
      else:
        self.__spi.frequency(5 * (10 ** 6));
        
      if (params['mode'] == 0):
        self.__spi.mode(mraa.SPI_MODE0);
      elif (params['mode'] == 1):
        self.__spi.mode(mraa.SPI_MODE1);
      elif (params['mode'] == 2):
        self.__spi.mode(mraa.SPI_MODE2);
      elif (params['mode'] == 3):
        self.__spi.mode(mraa.SPI_MODE3);
        
      if ("lsbmode" in params):
        self.__spi.lsbmode(params['lsbmode']);
        
      return True;
        
    # SPI functions
    def transfer(self, val):
      return self.__spi.writeByte(val);
                    