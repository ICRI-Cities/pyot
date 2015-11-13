#
# PyoT Davis Weather Station
#
# Michael Rosen
# mrrosen
# 16-10-2015
#

import os
import struct

from pyotlib.classes import *
import pyotlib.printlib as pr

# Function to make peripheral
def create(params):
  return DavisWS(params);
  
class DavisWS(peripheral.Peripheral):

  # Build function, add sensors to endpoints
  def build(self, params):
    self.endpoints.add("root", DavisWS.HostSensor);
    self.endpoints.add("barometer", DavisWS.Sensor);
    self.endpoints.add("inside_temperature", DavisWS.Sensor);
    self.endpoints.add("inside_humidity", DavisWS.Sensor);
    self.endpoints.add("outside_temperature", DavisWS.Sensor);
    self.endpoints.add("wind_speed", DavisWS.Sensor);
    self.endpoints.add("10_min_avg_wind_speed", DavisWS.Sensor);
    self.endpoints.add("wind_direction", DavisWS.Sensor);
    self.endpoints.add("outside_humidity", DavisWS.Sensor);
    self.endpoints.add("rain_rate", DavisWS.Sensor);
    self.endpoints.add("uv", DavisWS.Sensor);
    self.endpoints.add("solar_radiation", DavisWS.Sensor);
    self.endpoints.add("storm_rain", DavisWS.Sensor);
    self.endpoints.add("day_rain", DavisWS.Sensor);
    self.endpoints.add("month_rain", DavisWS.Sensor);
    self.endpoints.add("year_rain", DavisWS.Sensor);
    self.endpoints.add("day_et", DavisWS.Sensor);
    self.endpoints.add("month_et", DavisWS.Sensor);
    self.endpoints.add("year_et", DavisWS.Sensor);
    self.endpoints.add("transmitter_battery_status", DavisWS.Sensor);
    self.endpoints.add("console_battery_voltage", DavisWS.Sensor);
    return;
  
  class HostSensor(peripheral.GroupSensor):
  
    def connect(self, params):
      # As the root sensor, you need to grab the UART port
      self._serial = self.platform.find(params['port'], self);

      if (self._serial == None):
        pr.Wrn("DWS: Failed to find UART port '%s'" % params['port']);
        return;
      
      # Find the USB port
      usbPort = None;
      for f in os.listdir("/dev"):
        if (f.startswith("ttyUSB")):
          usbPort = "/dev/" + f;
          break;
      
      if (usbPort == None):
        pr.Wrn("DWS: No USB Serial port found in /dev");
        self._serial = None;
        return;
      
      if (not(self._serial.request({'baudrate': 19200, 'port': usbPort, 'timeout': params['timeout']}))):
        pr.Wrn("DWS: Failed to connect to given UART port");
        self._serial = None;
        return;
        
      return;
      
    def read(self):
      if (self._serial != None):
        pr.Dbg("DWS: Reading from sensor...");
        
        self._serial.write("LOOP 1\n\r");
        
        packet = self._serial.read(100);
        
        if (packet == None):
          pr.Wrn("DWS: Failed to read packet");
          return None;
        
        # Trim off ACK
        loop = packet[1:];
        data = dict();
        
        data['barometer']                    = self.getValueFromLoop(loop, 7, 'h', co=0.001);
        data['inside_temperature']           = self.FtoC(self.getValueFromLoop(loop, 9, 'h', co=0.1), 5);
        data['inside_humidity']              = self.getValueFromLoop(loop, 11, 'B', co=0.01);
        data['outside_temperature']          = self.FtoC(self.getValueFromLoop(loop, 12, 'h', co=0.1), 5);
        data['wind_speed']                   = self.getValueFromLoop(loop, 14, 'B');
        data['10_min_avg_wind_speed']        = self.getValueFromLoop(loop, 15, 'B');
        data['wind_direction']               = self.getValueFromLoop(loop, 16, 'H');
        data['outside_humidity']             = self.getValueFromLoop(loop, 33, 'B', co=0.01);
        data['rain_rate']                    = self.getValueFromLoop(loop, 41, 'H');
        data['uv']                           = self.getValueFromLoop(loop, 43, 'B');
        data['solar_radiation']              = self.getValueFromLoop(loop, 44, 'H');
        data['storm_rain']                   = self.getValueFromLoop(loop, 46, 'H', co=0.01);
        data['day_rain']                     = self.getValueFromLoop(loop, 50, 'H', co=0.01);
        data['month_rain']                   = self.getValueFromLoop(loop, 52, 'H', co=0.01);
        data['year_rain']                    = self.getValueFromLoop(loop, 54, 'H', co=0.01);
        data['day_et']                       = self.getValueFromLoop(loop, 56, 'H', co=0.001);
        data['month_et']                     = self.getValueFromLoop(loop, 58, 'H', co=0.01);
        data['year_et']                      = self.getValueFromLoop(loop, 60, 'H', co=0.01);
        data['transmitter_battery_status']   = self.getValueFromLoop(loop, 86, 'B');
        data['console_battery_voltage']      = self.getValueFromLoop(loop, 87, 'H', co=0.005859);
        
        return data;
        
      # Failed to read from sensor
      pr.Wrn("DWS: Failed to connect to serial");
      return None; 
    
    # Parses out data from the packet
    def getValueFromLoop(self, loop, offset, valType, co=1, off=0):
      return round(((struct.unpack_from(valType, loop, offset)[0] * co) + off), 5);

    # Temperature conversion functions
    def FtoC(self, temp, precision):
      return round(((temp - 32.0) * 5.0 / 9.0), precision);
  
    def CtoF(self, temp, precision):
      return round(((temp * 9.0 / 5.0) + 32.0), precision);
    
  class Sensor(peripheral.Sensor):
    
    def connect(self, params):
      self._root = self.platform.find(".:root", self);
      return;
    
    def read(self):
      pr.Dbg("DWS: Reading %s..." % self.name());
      val = self._root.read();
      if (val != None):
        return val[self.name()];
      else:
        pr.Wrn("DWS: Failed to read %s" % self.name());
        return None;
