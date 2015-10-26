#
# PyoT HC SR04 Arduino sensor class
#
# Michael Rosen
# mrrosen
# 26-10-2015
#

from pyotlib.classes import *
import pyotlib.printlib as pr

# Function to make peripheral
def create(params):
  return HC_SR04(params);
  
class HC_SR04(peripheral.Peripheral):

  # Build function, add sensors to endpoints
  def build(self, params):
    self.endpoints.add("distance", HC_SR04.Sensor);
    return;
    
  class Sensor(peripheral.GroupSensor):
  
    def connect(self, params):
      # As the root sensor, you need to grab the spi port
      self._i2c = self.platform.find(params['port'], self);

      if (self._i2c == None):
        pr.Wrn("HC-SR04: Failed to find I2C port '%s'" % params['port']);
        return;
      
      if (not(self._i2c.request())):
        pr.Wrn("HC-SR04: Failed to connect to given I2C port");
        self._i2c = None;
        return;
        
      return;
      
    def init(self, params):
      if (self._i2c != None):
        self._i2c.setAddr(params['addr']);
      return;
      
    def read(self):
      if (self._i2c != None):
        pr.Dbg("HC-SR04: Sending read request...");
        
        self._i2c.writeReg(0x3, 0x1);
        while (self._i2c.readReg(0x3) != 0x80):
          pass;
          
        pr.Dbg("HC-SR04: Got value back!");
        val = self._i2c.readReg(0x4);
        val += self._i2c.readReg(0x5);
        val += self._i2c.readReg(0x6);
        val += self._i2c.readReg(0x7);
        
        # Convert from cm to m
        return (val / 100.0);
        
      # Failed to read from sensor
      return None;

    

