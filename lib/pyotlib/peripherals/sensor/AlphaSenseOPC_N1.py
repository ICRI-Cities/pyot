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

  # Build function, add sensors to endpoints
  def build(self, params):
    self.endpoints.add("root", AlphaSenseOPC_N1.HostSensor);
    self.endpoints.add("pm10", AlphaSenseOPC_N1.Sensor);
    self.endpoints.add("pm25", AlphaSenseOPC_N1.Sensor);
    self.endpoints.add("pm100", AlphaSenseOPC_N1.Sensor);
    return;
    
  class HostSensor(peripheral.GroupSensor):
  
    def connect(self, params):
      # As the root sensor, you need to grab the spi port
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
        pr.Dbg("OPC - N1: Turning on fan...");
        self._spi.transfer(0x0C);
        
      self._timeBetweenSamples = params['minTimeBetweenSamples'];
      self._lastRead = 0;
      self._lastReading = None;

      return;
      
    def read(self):
      if (self._spi != None):
        if ((self._lastReading == None) or (time.time() > (self._lastRead + self._timeBetweenSamples))):
          pr.Dbg("OPC - N1: Reading from sensor...");
        
          # Be sure the fan is on
          self._spi.transfer(0x0C);
          time.sleep(0.1);
        
          # Send the command to read the data
          self._spi.transfer(0x30);
          time.sleep(0.006);
        
          v = [];
          for i in xrange(62):
            v.append(self._spi.transfer(0xC0));
            time.sleep(0.000008);
        
          pm10 = self.bytelistToFloat(v[50:54]);
          pm25 = self.bytelistToFloat(v[54:58]);
          pm100 = self.bytelistToFloat(v[58:62]);
          self._lastReading = {'pm10': pm10, 'pm25': pm25, 'pm100': pm100};
          
          self._lastRead = time.time();
          
        pr.Dbg("OPC - N1: Returning sensor data");
        return self._lastReading;
        
      # Failed to read from sensor
      return None;
      
    def bytelistToFloat(self, list):
      v = list[3] + (list[2] << 8) + (list[1] << 16) + (list[0] << 24);
      return struct.unpack("f", struct.pack("!I", v))[0];
    
  class Sensor(peripheral.Sensor):
    
    def connect(self, params):
      self._root = self.platform.find(".:root", self);
      return;
    
    def read(self):
      pr.Dbg("OPC - N1: Reading %s..." % self.name());
      val = self._root.read();
      if (val != None):
        return val[self.name()];
      else:
        return None;

