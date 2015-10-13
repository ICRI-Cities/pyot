#
# PyoT AlphaSense OPC-N1 sensor class
#
# Michael Rosen
# mrrosen
# 12-10-2015
#
# Acknowledge: David Crellin
#

import time
import struct

from pyotlib.platform import *
from pyotlib.classes import *
from pyotlib.printlib import *

# Function to make peripheral
def create(params):
  return AlphaSenseOPC_N1(params);
  
class AlphaSenseOPC_N1(peripheral.Peripheral):

  # Build function, add comm to endpoints
  def build(self, params):
    self.endpoints.add("root", AlphaSenseOPC_N1.HostSensor);
    self.endpoints.add("pm10", AlphaSenseOPC_N1.Sensor);
    self.endpoints.add("pm25", AlphaSenseOPC_N1.Sensor);
    self.endpoints.add("pm100", AlphaSenseOPC_N1.Sensor);
    return;
    
  class HostSensor(peripheral.Sensor):
  
    def connect(self, params):
      global platform;
     
      # As the root sensor, you need to grab the 
      self._spi = platform.find(params['port']);
      
      if (self._spi == None):
        return;
      
      if (not(self._spi.request({'frequency': 300000, 'mode': 1}))):
        self._spi = None;
        return;
        
      return;
    
    def init(self, params):
      # Turn on the fan
      if (self._spi != None):
        self._spi.transfer(0x0C);
        
      return;
      
    def read(self):
      if (self._spi != None):
        self._spi.transfer(0x30);
        time.sleep(0.006);
        
        v = [];
        for i in xrange(62):
          v.append(self._spi.transfer(0xC0));
          time.sleep(0.000008);
        
        pm10 = self.bytelistToFloat(v[50:54]);
        pm25 = self.bytelistToFloat(v[54:58]);
        pm100 = self.bytelistToFloat(v[58:62]);
        
        return {'pm10': pm10, 'pm25': pm25, 'pm100': pm100};
    
    def bytelistToFloat(self, list):
      v = list[3] + (list[2] << 8) + (list[1] << 16) + (list[0] << 24);
      return struct.unpack("f", struct.pack("!I", v))[0];
    
  class Sensor(peripheral.Sensor):
    
    def connect(self, params):
      global platform;
      self._root = platform.find(".:root");
      return;
    
    def read(self):
      return self._root.read()[self.name()];
