#
# PyoT Print Functions
#
# Michael Rosen
# mrrosen
# 12-10-2015
#

import traceback

# Print commands
def prMsg(s):
  print("-I- %s" % s);
  return;
  
def prWrn(s):
  print("-W- %s" % s);
  return;
  
def prErr(s):
  print("-E- %s" % s);
  if (debug):
    traceback.print_exc();
  return;
  
def prDbg(s):
  global debug;
  if (debug):
    print("-D- %s" % s);
  return;