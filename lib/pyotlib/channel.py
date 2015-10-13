#
# PyoT Channel
#
# Michael Rosen
# mrrosen
# 12-10-2015
#

import Queue
import threading

# A circular buffer of values between the sender and receiver
class Channel:

  def __init__(self):
    self.__queue = Queue.Queue(2048*1024);
    self.__lock = threading.Lock();
    
  def lock(self):
    self.__lock.acquire();
    return;

  def unlock(self):
    self.__lock.release();
    return;    
  
  def empty(self):
    return self.__queue.empty();
    
  def full(self):
    return self.__queue.full();
    
  def put(self, i):
    if (self.__queue.full()):
      self.__queue.get();
    self.__queue.put(i);
    return;
    
  def get(self):
    if (self.__queue.empty()):
      return None;
    else:
      return self.__queue.get();
      
  def size(self):
    return self.__queue.qsize();