#
# PyoT Tree
#
# Michael Rosen
# mrrosen
# 12-10-2015
#

import importlib

class Tree(object):
  
  def __init__(self, params):
    # Create platform
    module = importlib.import_module("pyotlib.peripherals." + params['class']);
    newParams = dict(params);
    newParams['path'] = "/";
    newParams['parent'] = None;
    self.__head = module.create(newParams);
    
  # Function for running the phases
  def build(self):
    self.__head._build();
    return;
  
  def connect(self):
    self.__head.__connect();
    return;
    
  def init(self):
    self.__head.__init();
    return;
    
  # Return the node described by path
  def find(self, obj, path):
    if (path[0] != "/"):
      return obj.__find("/" + path);
    else:      
      return self.__head.__find(path);
  
class Endpoints(object):

  def __init__(self, parent, path, params):
    self.__parent = parent;
    self.__path = path;
    self.__params = params;
    
    self.__endpoints = dict();
    
  def add(self, name, type):
    if (name in self.__endpoints):
      return None;
      
    if (name in self.__params):
      params = self.__params[name];
    else:
      params = {'build': {}, 'connect': {}, 'init': {}};
      
    self.__endpoints[name] = type(self.__parent, self.__path, name, params);
    
    return self.__endpoints[name];
    
  def find(self, name):
   if (name in self.__endpoints):
     return self.__endpoints[name];
     
   return None;
    
  # Phases
  def build(self):
    for ep in self.__endpoints:
      self.__endpoints[ep].build(self.__endpoints[ep].__params['build']);
    return;
    
  def connect(self):
    for ep in self.__endpoints:
      self.__endpoints[ep].connect(self.__endpoints[ep].__params['connect']);
    return;
    
  def init(self):
    for ep in self.__endpoints:
      self.__endpoints[ep].init(self.__endpoints[ep].__params['init']);
    return;
