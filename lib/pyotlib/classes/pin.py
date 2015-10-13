#
# PyoT Pins Class
#
# Michael Rosen
# mrrosen
# 09-10-2015
#

# Class for handling pins for peripherals
class Pins(object):
  
  # Create object to keep track of peripheral pins
  def __init__(self, pinlist):
    self._freepins = set(pinlist);
    
  # Request pins
  def request(self, obj):
    if (obj._pinSet.issubset(self._freepins)):
      obj._pinSet._freepins = self._freepins.difference(obj._pinSet);
      return True;
    
    return False;
      
  # Assign pins to object
  def assign(self, obj, pins):
    obj.pins = self;
    obj._pinSet = set(pins);
    return;
