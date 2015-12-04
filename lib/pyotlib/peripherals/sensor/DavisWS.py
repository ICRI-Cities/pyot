#
# PyoT Davis Weather Station
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
      
    def init(self, params):
      self._timeBetweenSamples = 10;
      self._lastRead = 0;
      self._data = None;
      
      return;
      
    def read(self):
      if (self._serial != None):
        if ((self._data == None) or (time.time() > (self._lastRead + self._timeBetweenSamples))):
          pr.Dbg("DWS: Reading from sensor...");
          
          self._serial.write("LOOP 1\n\r");
          
          time.sleep(0.1);
          
          packet = self._serial.read(100);
          
          if (packet == None):
            pr.Wrn("DWS: Failed to read packet");
            return None;
          
          # Trim off ACK
          loop = packet[1:];
          if (not(self.crcCheck(loop))):
            pr.Wrn("DWS: CRC Check Failed!");
            return None;
            
          self._data = dict();
          
          self._data['barometer']                    = self.getValueFromLoop(loop, 7, 'h', co=0.00254);
          self._data['inside_temperature']           = self.FtoC(self.getValueFromLoop(loop, 9, 'h', co=0.1), 5);
          self._data['inside_humidity']              = self.getValueFromLoop(loop, 11, 'B', co=0.01);
          self._data['outside_temperature']          = self.FtoC(self.getValueFromLoop(loop, 12, 'h', co=0.1), 5);
          self._data['wind_speed']                   = self.getValueFromLoop(loop, 14, 'B', co=1.61);
          self._data['10_min_avg_wind_speed']        = self.getValueFromLoop(loop, 15, 'B', co=1.61);
          self._data['wind_direction']               = self.getValueFromLoop(loop, 16, 'H');
          self._data['outside_humidity']             = self.getValueFromLoop(loop, 33, 'B', co=0.01);
          self._data['rain_rate']                    = self.getValueFromLoop(loop, 41, 'H', co=0.05);
          self._data['uv']                           = self.getValueFromLoop(loop, 43, 'B');
          self._data['solar_radiation']              = self.getValueFromLoop(loop, 44, 'H');
          self._data['storm_rain']                   = self.getValueFromLoop(loop, 46, 'H', co=0.0254);
          self._data['day_rain']                     = self.getValueFromLoop(loop, 50, 'H', co=0.05);
          self._data['month_rain']                   = self.getValueFromLoop(loop, 52, 'H', co=0.05);
          self._data['year_rain']                    = self.getValueFromLoop(loop, 54, 'H', co=0.05);
          self._data['day_et']                       = self.getValueFromLoop(loop, 56, 'H', co=0.00254);
          self._data['month_et']                     = self.getValueFromLoop(loop, 58, 'H', co=0.0254);
          self._data['year_et']                      = self.getValueFromLoop(loop, 60, 'H', co=0.0254);
          self._data['transmitter_battery_status']   = self.getValueFromLoop(loop, 86, 'B');
          self._data['console_battery_voltage']      = self.getValueFromLoop(loop, 87, 'H', co=0.005859);
          
          self._lastRead = time.time();
        
        pr.Dbg("DWS: Returning data");
        return self._data;
        
      # Failed to read from sensor
      pr.Wrn("DWS: Failed to connect to serial");
      return None; 
      
    # Checks the CRC of a packet (returns True on success)
    def crcCheck(self, v):
      crc = 0;
      crcTable = [0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
                  0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef,
                  0x1231, 0x0210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6,
                  0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de,
                  0x2462, 0x3443, 0x0420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485,
                  0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d,
                  0x3653, 0x2672, 0x1611, 0x0630, 0x76d7, 0x66f6, 0x5695, 0x46b4,
                  0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc,
                  0x48c4, 0x58e5, 0x6886, 0x78a7, 0x0840, 0x1861, 0x2802, 0x3823,
                  0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b,
                  0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0x0a50, 0x3a33, 0x2a12,
                  0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a,
                  0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0x0c60, 0x1c41,
                  0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49,
                  0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0x0e70,
                  0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78,
                  0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f,
                  0x1080, 0x00a1, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
                  0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e,
                  0x02b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256,
                  0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d,
                  0x34e2, 0x24c3, 0x14a0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
                  0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c,
                  0x26d3, 0x36f2, 0x0691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634,
                  0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab,
                  0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x08e1, 0x3882, 0x28a3,
                  0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
                  0x4a75, 0x5a54, 0x6a37, 0x7a16, 0x0af1, 0x1ad0, 0x2ab3, 0x3a92,
                  0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9,
                  0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0x0cc1,
                  0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8,
                  0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0x0ed1, 0x1ef0];
                  
      for c in v:
        lC = ord(c) & 0xff;
        lCrc = crc & 0xffff;
        crc = crcTable[((lCrc >> 8) ^ lC) & 0xff] ^ ((lCrc << 8) & 0xffff);
        
      return (crc == 0);
    
    # Parses out data from the packet, return None if read all ones
    def getValueFromLoop(self, loop, offset, valType, co=1, off=0):
      val = struct.unpack_from(valType, loop, offset)[0];
      if (((valTpe in 'hH') and self.allOnes(val, 16)) or ((valType in 'bB') and self.allOnes(val, 8))):
        pr.Dbg("DWS: Failed to read a valid value from the remote station (console returned all ones!)");
        return None;
      return round(((val * co) + off), 5);
      
    # Determine is value is all ones
    def allOnes(self, v, l):
      for x in xrange(l):
        if (((v >> x) & 0x1) == 0):
          return False;
      return True;

    # Temperature conversion functions
    def FtoC(self, temp, precision):
      if (temp == None):
        return None;
      return round(((temp - 32.0) * 5.0 / 9.0), precision);
  
    def CtoF(self, temp, precision):
      if (temp == None):
        return None;
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
