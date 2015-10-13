#
# PyoT Interface Base Classes
#
# Michael Rosen
# mrrosen
# 09-10-2015
#

from abc import *
from pyotlib.classes.peripheral import Port
import pyotlib.printlib as pr

# Base class UART ports
class UART(Port):
  __metaclass__ = ABCMeta;  
  
  @abstractmethod
  def read(self, bytes):
    pass;
    
  @abstractmethod
  def write(self, s):
    pass;
    
# Base class SPI ports
class SPI(Port):
  __metaclass__ = ABCMeta;
  
  @abstractmethod
  def transfer(self, val):
    pass;

# Base class I2C ports
class I2C(Port):
  __metaclass__ = ABCMeta;
  
  @abstractmethod
  def setAddr(self, addr):
    pass;
  
  @abstractmethod
  def readReg(self, reg):
    pass;
    
  @abstractmethod
  def writeReg(self, reg, val):
    pass;
    
# Base class AIN ports
class AIN(Port):
  __metaclass__ = ABCMeta;
  
  @abstractmethod
  def read(self):
    pass;
    
# Base class GPIO ports
class GPIO(Port):
  __metaclass__ = ABCMeta;
  
  @abstractmethod
  def read(self):
    pass;
    
  @abstractmethod
  def write(self, val):
    pass;
