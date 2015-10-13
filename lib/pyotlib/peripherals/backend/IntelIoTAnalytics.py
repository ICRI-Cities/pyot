#
# PyoT Intel IoT Analytics backend
#
# Michael Rosen
# mrrosen
# 12-10-2015
#

from pyotlib.classes import *
import pyotlib.printlib as pr

# Function to make peripheral
def create(params):
  return IntelIoTAnalytics(params);
  
class IntelIoTAnalytics(peripheral.Peripheral):

  # Build function, add comm to endpoints
  def build(self, params):
    self.endpoints.add("mqtt", IntelIoTAnalytics.MQTT);
    return;
    
  class MQTT(peripheral.Comm):
  
    def init(self, params):
      return;
    
    def send(self, val):
      print(val);
      return True;
    
    def poll(self):
      return None;