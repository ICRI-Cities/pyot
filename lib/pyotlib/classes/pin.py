#
# PyoT Pins Class
#
# Michael Rosen
# mrrosen
# 09-10-2015
#

# Class for handling pins for peripherals
class Pins:
  
  # Create object to keep track of peripheral pins
  def __init__(self, pinlist):
    self.__freepins = set(pinlist);
    
  # Request pins
  def request(self, obj):
    if (obj.__pinSet.issubset(self.__freepins)):
      obj.__pinSet.__freepins = self.__freepins.difference(obj.__pinSet);
      return True;
    
    return False;
      
  # Assign pins to object
  def assign(self, obj, pins):
    obj.pins = self;
    obj.__pinSet = set(pins);
    return;
