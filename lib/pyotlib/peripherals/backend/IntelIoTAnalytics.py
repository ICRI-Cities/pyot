#
# PyoT Intel IoT Analytics backend
#
# Michael Rosen
# mrrosen
# 12-10-2015
#

import json
import time
import paho.mqtt.client as mqtt

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
  
    def build(self, params):
      self._gotMessages = [];
  
    def init(self, params):
      self._token = params['token'];
      self._accountID = params['accountID'];
      self._deviceID = params['deviceID'];
      self._qos = params['qos'];
      self._messageTimeout = params['timeout'];
    
      self._mqtt = mqtt.Client();
      
      self._mqtt.tls_set(ca_certs=params['certs']);
      self._mqtt.tls_insecure_set(True);
      
      self._mqtt.username_pw_set(self._accountID, self._token);
      self._mqtt.connect(params['broker'], params['brokerPort']);
      
      self._mqtt.on_publish = self.publishCallback;
      return;
    
    def send(self, val):
      print(val);
      
      ts = val['ts'];
      comp = val['name'];
      data = val['val'];
      
      topic = "server/metric/%s/%s" % (self._accountID, self._deviceID);

      # (succ, mid) = self._mqtt.publish(topic, json.dumps(packet), qos=self._qos);
      #
      # start = time.time();
      # while (time.time() < (start + self._messageTimeout)):
      #   if (mid in self._gotMessages):
      #     self._gotMessages.remove(mid);
      #     return True;
      #
      # return False;
      
      return True;
      
    def publishCallback(self, client, userdata, mid):
      self._gotMessages.append(mid);
      return;
    
    def poll(self):
      return None;