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
class Channel(object):

  def __init__(self):
    self._queue = Queue.Queue(2048*1024);
    self._lock = threading.Lock();
    
  def lock(self):
    self._lock.acquire();
    return;

  def unlock(self):
    self._lock.release();
    return;    
  
  def empty(self):
    return self._queue.empty();
    
  def full(self):
    return self._queue.full();
    
  def put(self, i):
    if (self._queue.full()):
      self._queue.get();
    self._queue.put(i);
    return;
    
  def get(self):
    if (self._queue.empty()):
      return None;
    else:
      return self._queue.get();
      
  def size(self):
    return self._queue.qsize();