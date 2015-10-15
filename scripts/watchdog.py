#
# PyoT Watchdog
#
# Michael Rosen
# mrrosen
# 15-10-2015
#

import os
import time
import pyotlib.printlib as pr

while (True):
  pr.Msg("Pinging www.intel.com to check internet");
  ret = os.system("ping -c1 -w1 www.intel.com");
  
  if (ret != 0):
    pr.Err("Failed to reach www.intel.com; internet down!");
    
  ret = os.system("ps | grep pyot | grep -v grep ");
  
  if (ret != 0):
    pr.Err("pyot process crashed!");
    
  pr.Msg("All is well, sleeping for 120 seconds...");
  time.sleep(120);