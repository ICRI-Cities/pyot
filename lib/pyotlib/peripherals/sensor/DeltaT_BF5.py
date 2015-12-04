#
# PyoT DeltaT Solar Sensor
#
# Michael Rosen
# mrrosen
# 16-10-2015
#

import os
import time
import struct

from pyotlib.classes import *
import pyotlib.printlib as pr

# Function to make peripheral
def create(params):
  return DeltaT_BF5(params);
  
class DeltaT_BF5(peripheral.Peripheral):

  # Build function, add sensors to endpoints
  def build(self, params):
    self.endpoints.add("root", DeltaT_BF5.HostSensor);
    self.endpoints.add("total", DeltaT_BF5.Sensor);
    self.endpoints.add("diffuse", DeltaT_BF5.Sensor);
    return;  
  
  class HostSensor(peripheral.GroupSensor):
  
    def connect(self, params):
      # As the root sensor, you need to grab the UART port
      self._serial = self.platform.find(params['port'], self);

      if (self._serial == None):
        pr.Wrn("BF5: Failed to find UART port '%s'" % params['port']);
        return;
      
      if (not(self._serial.request({'baudrate': 9600, 'port': "/dev/ttyS0", 'timeout': params['timeout']}))):
        pr.Wrn("BF5: Failed to connect to given UART port");
        self._serial = None;
        return;
        
      return;
      
    def init(self, params):
      self._timeBetweenSamples = 10;
      self._lastRead = 0;
      self._data = None;
      
      return;
      
    def read(self):
      if (self._serial != None):
        if ((self._data == None) or (time.time() > (self._lastRead + self._timeBetweenSamples))):
          pr.Dbg("BF5: Reading from sensor...");
          
          self._serial.write("S");
          
          time.sleep(0.1);
          
          packet = self._serial.read(19);
          
          if (packet == None):
            pr.Wrn("BF5: Failed to read packet");
            return None;
          
          st = packet[1:-1];
          vals = []
          while (st.find(",") != -1):
            vals.append(float(st[:st.find(",")]));
            st = st[(st.find(",") + 1):];
            
          if (len(vals) != 2):
            pr.Wrn("BF5: Failed to parse packet");
            return None;
            
          self._data = dict();
          self._data['total'] = vals[0];
          self._data['diffuse'] = vals[1];
          
          self._lastRead = time.time();
        
        pr.Dbg("BF5: Returning data");
        return self._data;
        
      # Failed to read from sensor
      pr.Wrn("BF5: Failed to connect to serial");
      return None; 
    
  class Sensor(peripheral.Sensor):
    
    def connect(self, params):
      self._root = self.platform.find(".:root", self);
      return;
    
    def read(self):
      pr.Dbg("BF5: Reading %s..." % self.name());
      val = self._root.read();
      if (val != None):
        return val[self.name()];
      else:
        pr.Wrn("BF5: Failed to read %s" % self.name());
        return None;
