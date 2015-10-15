#
# PyoT Print Functions
#
# Michael Rosen
# mrrosen
# 12-10-2015
#

import sys
import traceback

debug = False;

# Print commands
def Msg(s):
  print("%20s: -I- %s" % (sys.argv[0], s));
  return;
  
def Wrn(s):
  print("%20s: -W- %s" % (sys.argv[0], s);
  return;
  
def Err(s):
  global debug;
  print("%20s: -E- %s" % (sys.argv[0], s));
  if (debug):
    traceback.print_exc();
  return;
  
def Dbg(s):
  global debug;
  if (debug):
    print("%20s: -D- %s" % (sys.argv[0], s));
  return;