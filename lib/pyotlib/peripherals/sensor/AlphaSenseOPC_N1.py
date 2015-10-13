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

from pyotlib.classes import *
import pyotlib.printlib as pr

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
      # As the root sensor, you need to grab the 
      self._spi = self.platform.find(params['port'], self);

      if (self._spi == None):
        pr.Wrn("OPC - N1: Failed to find SPI port '%s'" % params['port']);
        return;
      
      if (not(self._spi.request({'frequency': 300000, 'mode': 1}))):
        pr.Wrn("OPC - N1: Failed to connect to given SPI port");
        self._spi = None;
        return;
        
      return;
    
    def init(self, params):
      # Turn on the fan
      if (self._spi != None):
        for i in xrange(5):
          pr.Dbg("OPC - N1: Turning on fan... (try: %d)" % i);
          r = self._spi.transfer(0x0C);
          pr.Dbg("OPC - N1: ret = %d" % r);
          time.slepp(0.1);
      return;
      
    def read(self):
      if (self._spi != None):
        pr.Dbg("OPC - N1: Reading from sensor...");
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
      self._root = self.platform.find(".:root", self);
      return;
    
    def read(self):
      pr.Dbg("OPC - N1: reading...");
      return 1;
      return self._root.read()[self.name()];
