#
# PyoT Davis Weather Station
#
# Michael Rosen
# mrrosen
# 16-10-2015
#



from pyotlib.classes import *
import pyotlib.printlib as pr

# Function to make peripheral
def create(params):
  return DavisWS(params);
  
class DavisWS(peripheral.Peripheral):

  # Build function, add sensors to endpoints
  def build(self, params):
    self.endpoints.add("root",DavisWS.HostSensor);
    self.endpoints.add("pm10", DavisWS.Sensor);
    self.endpoints.add("pm25", DavisWS.Sensor);
    self.endpoints.add("pm100", DavisWS.Sensor);
    return;
  
  class HostSensor(peripheral.Sensor):
  
    def connect(self, params):
      # As the root sensor, you need to grab the UART port
      self._serial = self.platform.find(params['port'], self);

      if (self._serial == None):
        pr.Wrn("DWS: Failed to find UART port '%s'" % params['port']);
        return;
      
      if (not(self._serial.request({'baudrate': 19200, 'type': "USB0"}))):
        pr.Wrn("DWS: Failed to connect to given UART port");
        self._spi = None;
        return;
        
      return;
      
    def read(self):
      if (self._uart != None):
        pr.Dbg("DWS: Reading from sensor...");
        
        self._uart.write("LOOP 1\n\r");
        
        packet = self._uart.read(100);
        
        if (packet == None):
          return None;
        

    
  class Sensor(peripheral.Sensor):
    
    def connect(self, params):
      self._root = self.platform.find(".:root", self);
      return;
    
    def read(self):
      pr.Dbg("OPC - N1: reading...");
      return self._root.read()[self.name()];