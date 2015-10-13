#
# PyoT Print Functions
#
# Michael Rosen
# mrrosen
# 12-10-2015
#

import traceback

debug = [False];

# Print commands
def prMsg(s):
  print("-I- %s" % s);
  return;
  
def prWrn(s):
  print("-W- %s" % s);
  return;
  
def prErr(s):
  global debug;
  print("-E- %s" % s);
  if (debug[0]):
    traceback.print_exc();
  return;
  
def prDbg(s):
  global debug;
  if (debug[0]):
    print("-D- %s" % s);
  return;