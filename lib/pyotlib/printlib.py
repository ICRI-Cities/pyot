#
# PyoT Print Functions
#
# Michael Rosen
# mrrosen
# 12-10-2015
#

import traceback

debug = False;

# Print commands
def Msg(s):
  print("-I- %s" % s);
  return;
  
def Wrn(s):
  print("-W- %s" % s);
  return;
  
def Err(s):
  global debug;
  print("-E- %s" % s);
  if (debug):
    traceback.print_exc();
  return;
  
def Dbg(s):
  global debug;
  if (debug):
    print("-D- %s" % s);
  return;