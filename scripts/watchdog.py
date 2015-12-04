#
# PyoT Watchdog
#
# Michael Rosen
# mrrosen
# 15-10-2015
#

import os
import sys
import time
import getopt
import datetime
import traceback
import pyotlib.printlib as pr

def reboot():
  pr.Wrn("REBOOTING!");
  
  try:
    # Rotake the logs
    t = time.time();
    epochTime = str(int(round(t * 1000)));
    humanTime = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d_%H:%M:%S');
    fname = "reboot_" + epochTime + "_" + humanTime + ".log";
  
    os.system("dmesg > logs/" + fname);
  
    logs = os.listdir("logs");
    while (len(logs) > 25):
      logs.sort();
      os.remove("logs/" + logs[0]);
      logs = os.listdir("logs");
  except:
    pass;

  os.system("reboot");
  return;
  
pr.Msg("Watchdog script is starting up!");
  
# Parse arguments
try:
  (options, args) = getopt.getopt(sys.argv, 'dt:', ['time=', 'debug']);
  pr.Msg(str(options));
except:
  traceback.print_exc();
  pr.Err("Bad commandline options");
  sys.exit(-1);

sleepTime = 3600;

for (o, a) in options:
  pr.Msg("Processing options %s %s" % (str(o), str(a)));
  if (o in ("-t", "--time")):
    sleepTime = int(a);
  elif (o in ("-d", "--debug")):
    pr.debug = True;
  
startTime = time.time();

while (True):
  pr.Msg("Pinging www.intel.com to check internet");
  ret = os.system("ping -c1 -w1 www.intel.com");
  
  if (ret != 0):
    pr.Err("Failed to reach www.intel.com; internet down!");
    reboot();
    
  pr.Msg("Checking to be sure pyot process is still running");
  ret = os.system("ps | grep pyot | grep -v grep ");
  
  if (ret != 0):
    pr.Err("pyot process crashed!");
    reboot();
    
  if (time.time() > (startTime + (24 * 3600))):
    pr.Wrn("Time for daily reboot!");
    reboot();
    
  pr.Msg("All is well, sleeping for %d seconds..." % sleepTime);
  time.sleep(sleepTime);