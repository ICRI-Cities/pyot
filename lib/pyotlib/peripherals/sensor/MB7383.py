#
# PyoT MB7383 Distance Sesnor
#
# Michael Rosen
# mrrosen
# 09-12-2015
#

from pyotlib.classes import *
import pyotlib.printlib as pr

# Function to make peripheral
def create(params):
  return MB7383(params);
  
class MB7383(peripheral.Peripheral):

  # Build function, add sensors to endpoints
  def build(self, params):
    self.endpoints.add("distance", MB7383.Sensor);
    return;
    
  class Sensor(peripheral.GroupSensor):
  
    def connect(self, params):
      # As the root sensor, you need to grab the UART port
      self._serial = self.platform.find(params['port'], self);

      if (self._serial == None):
        pr.Wrn("MB7383: Failed to find UART port '%s'" % params['port']);
        return;
      
      if (not(self._serial.request({'baudrate': 9600, 'timeout': params['timeout']}))):
        pr.Wrn("MB7383: Failed to connect to given UART port");
        self._serial = None;
        return;
        
      return;

      
    def read(self):
      if (self._serial != None):
        pr.Dbg("MB7383: Reading values");
        
        self._serial.emptyInput();
        val = self._serial.read(6);
        
        if (val != None):
          # Convert from mm to m
          return (int(val[1:-1]) / 1000.0);
        
      # Failed to read from sensor
      return None;
