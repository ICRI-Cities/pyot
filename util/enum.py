#
# Script to printout the endpoints for a given class
#
# Michael Rosen
# mrrosen
# 09-10-2015
#

import sys
import importlib

def main(args):
  if (len(args) != 1):
    print("Please provide a single class to enumerate");
    return;
  print("Enumerating endpoints for %s" % args[0]);
  module = importlib.import_module("pyotlib.peripherals." + args[0]);
  fake_params = {'platform': "", 
                 'parent': "", 
                 'name': "",
                 'path': "",
                 'params': {},
                 'peripherals': []};
  obj = modules.create(fake_params);
  obj.build();
  obj.endpoints.enumerate();
  return;
  
if (__name__ == "__main__"):
  main(sys.argv[1:]);