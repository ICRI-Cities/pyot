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
  
def pub(client, userdata, mid):
  pr.Dbg(" -- Got Message %d" % mid);
  return;
  
class IntelIoTAnalytics(peripheral.Peripheral):

  # Build function, add comm to endpoints
  def build(self, params):
    self.endpoints.add("mqtt", IntelIoTAnalytics.MQTT);
    return;
    
  class MQTT(peripheral.Comm):
  
    def build(self, params):
      self._gotMessages = [];
  
    def init(self, params):
      self._token = str(params['token']);
      self._accountID = str(params['accountID']);
      self._deviceID = str(params['deviceID']);
      self._qos = params['qos'];
      self._messageTimeout = params['timeout'];
    
      self._mqtt = mqtt.Client();
      
      self._mqtt.tls_set(ca_certs=params['certs']);
      self._mqtt.tls_insecure_set(True);
      
      self._mqtt.username_pw_set(self._accountID, self._token);
      r = self._mqtt.connect(str(params['broker']), str(params['brokerPort']));
      pr.Dbg("Get back conn: %s" % mqtt.error_string(r));
      
      self._mqtt.on_publish = pub;
      self._mqtt.on_log = self.log;
      
      r = self._mqtt.loop_start();
      if (r != None):
        pr.Dbg("Get back loop: %s %d" % (mqtt.error_string(r), r));
      return;
      
    def log(self, client, userdata, level, buf):
      pr.Dbg("EnableIoT - MQTT: %s" % buf);
      return;
    
    def send(self, val):
      print(val);
      
      ts = val['ts'];
      comp = val['name'];
      data = str(val['val']);
      
      topic = "server/metric/%s/%s" % (self._accountID, self._deviceID);
      
      packet = {
        'accountID': self._accountID,
        'did': self._deviceID,
        'on': ts,
        'count': 1,
        'data': [{'on': ts, 'value': data, 'cid': comp}]
      };
      pr.Dbg("Sending: %s \n\nto: %s" % (json.dumps(packet), str(topic)));
      (succ, mid) = self._mqtt.publish(topic, json.dumps(packet), qos=self._qos);
      pr.Dbg("Succ: %s, MID: %d" % (mqtt.error_string(succ), mid));
      start = time.time();
      while (time.time() < (start + self._messageTimeout)):
        if (mid in self._gotMessages):
          self._gotMessages.remove(mid);
          pr.Dbg("Success!");
          return True;
        time.sleep(0.5);
      pr.Dbg("Fail....");
      return False;
      
    def publishCallback(self, client, userdata, mid):
      self._gotMessages.append(mid);
      pr.Dbg("Got msg: %d" % mid);
      return;
    
    def poll(self):
      return None;