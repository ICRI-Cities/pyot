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
  def request(self, obj, pins=[]):
    if (len(pins) == 0):
      p = obj._pinSet;
    else:
      p = set(pins);
      
    if (p.issubset(self._freepins)):
      self._freepins = self._freepins.difference(p);
      return True;
    
    return False;
      
  # Assign pins to object
  def assign(self, obj, pins):
    obj.pins = self;
    obj._pinSet = set(pins);
    return;
    
  # Get the pins for the currently assigned object (as a list)
  def getPins(self, obj):
    return list(obj._pinSet);
