#
# PyoT Base Classes
#
# Michael Rosen
# mrrosen
# 09-10-2015
#

import importlib
from abc import *
from pyotlib.tree import Endpoints

# Base class for peripheral objects, includes a bunch of stuff for dealing with the tree structure
class Peripheral(object):
  
  def __init__(self, params):
    self.__path = params['path'];
    self.__parent = params['parent'];
    self.__name = params['name'];
    
    # Parse params
    if ("." in params['params']):
      self.__params = params['params']['.'];
    else:
      self.__params = {'build': {}, 'connect': {}, 'init': {}};
    
    # Create endpoints
    self.endpoints = Endpoints(self, self.fullname(), params['params']);
    
    # Create all peripherals    
    self.__peripherals = []
    for p in params['peripherals']:
      module = importlib.import_module("pyotlib.peripherals." + p['class']);
      newParams = dict(p);
      newParams['path'] = self.fullname();
      newParams['parent'] = self;
      self.__peripherals.append(module.create(newParams));
  
  # Recursive find method  
  def __find(self, path):
    # Take off the leading /
    p = path[1:];
    
    # If there is no longer a / in the path, we are the end (maybe)
    if (not("/" in p)):
      parts = p.split(":");
      if ((parts[0] == self.__name) or (parts[0] == ".")):
        if (len(parts) == 1):
          return self;
        else:
          return self.endpoints.find(parts[1]);
    else:
      # We are not the endpoint, strip off ourself (also checking if we were the proper place to go)
      parts = p.split("/");
      if ((parts[0] == self.__name) or (parts[0] == ".") or (parts[0] == "..") or (parts[0] == "")):
        newPath = p[len(parts[0]):];
        if ((parts[1] == self.__name) or (parts[1] == ".") or (parts[1] == "")):
          return self.__find(newPath);
        elif (parts[1] == ".."):
          return self.__parent.__find(newPath);
        else:
          for peripheral in self.__peripherals:
            if (parts[1] == peripheral.__name):
              return peripheral.__find(newPath);
    
    return None;
    
  def name(self):
    return self.__name;
   
  def path(self):
    return self.__path;
    
  def fullname(self):
    return (self.__path + "/" + self.__name); 
     
  #Phases
  
  def build(self, params):
    return;
    
  def __build(self):
    self.build(self.__params['build']);
    self.endpoints.build();
    
       
    for p in self.__peripherals:
      p.__build();
      
    return;
    
  def connect(self, params):
    return;
    
  def __connect(self):
    self.build(self.__params['connect']);
    self.endpoints.connect();
    
       
    for p in self.__peripherals:
      p.__connect();
      
    return;
    
  def init(self, params):
    return;
    
  def __init(self):
    self.build(self.__params['init']);
    self.endpoints.init();
    
    for p in self.__peripherals:
      p.__init();
      
    return;

# Endpoint base class
class Endpoint(object):
  
  def __init__(self, parent, path, name, params):
    self.__parent = parent;
    self.__path = path;
    self.__name = name;
    self.__params = params;
    
  def name(self):
    return self.__name;
    
  def path(self):
    return self.__path;
    
  def fullname(self):
    return (self.__path + ":" + self.__name);
    
  def __find(self, path):
    return self.__parent.__find(path);
  
  def build(self, params):
    return;
    
  def connect(self, params):
    return;
    
  def init(self, params):
    return;
    
  def request(self, params):
    return True;
  
# Base class for sensor objects
class Sensor(Endpoint):
  __metaclass__ = ABCMeta;
    
  @abstractmethod
  def read(self):
    pass;
   
# Base class for actuator objects
class Actuator(Endpoint):
  __metaclass__ = ABCMeta;

  @abstractmethod
  def write(self, val):
    pass;
    
# Base class for comm objects
class Comm(Endpoint):
  __metaclass__ = ABCMeta;
    
  @abstractmethod
  def send(self, vals):
    pass;
  
  @abstractmethod
  def poll(self):
    pass;
    
# Base class for port objects
class Port(Endpoint):
  pass;
