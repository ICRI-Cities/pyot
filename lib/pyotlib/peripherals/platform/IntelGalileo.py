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
import pyotlib.printlib as pr

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
    self.pins.assign(self.endpoints.add("uart2", GalileoPlatform.UART), [22]);
    self.pins.assign(self.endpoints.add("uart1", GalileoPlatform.UART), [0, 1]);
    
    return;
    
  # GPIO Class for Galileo (uses mraa to do everything)
  class GPIO(interface.GPIO):
      
    # Request function
    def request(self, params):
      if (not(self.pins.request(self))):
        return False;
    
      # Note, this should really go in build, but libmraa is stupid and wont work if other objects
      # are created inbetween...
      self._gpio = mraa.Gpio(self.pins.getPins(self)[0]);
    
      if ("mode" in params):
        if (params['mode'] == "PULLDOWN"):
          self._gpio.mode(mraa.MODE_PULLDOWN);
        elif (params['mode'] == "PULLUP"):
          self._gpio.mode(mraa.MODE_PULLUP);
          
          
      if (("dir" in params) and (params['dir'] == "OUT")):
        self._gpio.dir(mraa.DIR_OUT);
      else:
        self._gpio.dir(mraa.DIR_IN);
        
      return True;
    
    # GPIO functions    
    def write(self, val):
      self._gpio.write(val);
      return;
      
    def read(self):
      return self._gpio.read();
      
  # SPI Class for Galileo (uses mraa to do everything)
  class SPI(interface.SPI):
      
    # Request function
    def request(self, params):
      if (not(self.pins.request(self))):
        return False;
        
      # Note, this should really go in build, but libmraa is stupid and wont work if other objects
      # are created inbetween...
      self._spi = mraa.Spi(1);
      
      if ("frequency" in params):
        self._spi.frequency(params['frequency']);
      else:
        self._spi.frequency(5 * (10 ** 6));
        
      if (params['mode'] == 0):
        self._spi.mode(mraa.SPI_MODE0);
      elif (params['mode'] == 1):
        self._spi.mode(mraa.SPI_MODE1);
      elif (params['mode'] == 2):
        self._spi.mode(mraa.SPI_MODE2);
      elif (params['mode'] == 3):
        self._spi.mode(mraa.SPI_MODE3);
      
      if ("lsbmode" in params):
        self._spi.lsbmode(params['lsbmode']);
        
      #r = self._spi.writeByte(0x0c);
      #pr.Dbg("Test: %d" % r);
      return True;
        
    # SPI functions
    def transfer(self, val):
      return self._spi.writeByte(val);
      
  # UART Class for Galileo (uses pyserial to do everything)
  class UART(interface.UART):
  
    # Request function
    def request(self, params):
      if (not(self.pins.request(self))):
        return False;
      
      # Form dict with all params
      serialParams = {};
      if ("baudrate" in params):
        serialParams['baudrate'] = params['baudrate'];
      else:
        serialParams['baudrate'] = 9600;
      
      if ("timeout" in params):
        serialParams['timeout'] = params['timeout'];
      else:
        serialParams['timeout'] = 10;
        
      # Need to create serial object here to deal with params
      try:
        self._uart = serial.Serial(params['port'], 
                                   baudrate=serialParams['baudrate'], 
                                   timeout=serialParams['timeout']);
      except:
        return False;

      return True;

    # UART functions
    def read(self, bytes):
      val = self._uart.read(bytes);
      if (len(val) != bytes):
        return None;
      else:
        return val;
        
    def write(self, s):
      self._uart.write(s);
      self._uart.flush();
      return;
      