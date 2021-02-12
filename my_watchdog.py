from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import signal
import sys
import threading
import os

from utils import getFileName

import config
log = config.logger

def workWrapper(work, filePath, delete_after_work=config.delete_after_work):
  filename = getFileName(filePath)

  log.info('%s\t\tStart processing', filename)
  result = work(filePath)
  log.info('%s\t\tProcessing finished with result %s', filename, result)

  if delete_after_work and result:
    os.remove(filePath)

class EventHandler_WithLog(PatternMatchingEventHandler):
  def __init__(self,pattern, work, delete_after_work=config.delete_after_work):
    PatternMatchingEventHandler.__init__(self, patterns=[pattern], ignore_directories=True)
    self.work = work
    self.delete_after_work = delete_after_work

  def on_created(self, event, after_modification=False):
    super(EventHandler_WithLog, self).on_created(event)
    
    filename = getFileName(event.src_path)
    event_label = 'Detected'
    # if after_modification:
    #   event_label = 'Modificated'
    log.info("%s\t\t%s", filename, event_label)
    if self.work:
      workWrapper(self.work, event.src_path, self.delete_after_work)

  def on_deleted(self, event):
    super(EventHandler_WithLog, self).on_deleted(event)
    filename = getFileName(event.src_path)
    log.info("%s\t\tDone", filename)
  
  # def on_modified(self, event):
  #   super(EventHandler_WithLog, self).on_modified(event)
  #   self.on_created(event, True)
  #   # filename = ntpath.basename(event.src_path)
  #   # log.info("%s Done", filename)

class WatchDog(threading.Thread):
  def __init__(self, handlers):

    self.handlers =  handlers
    self.event = threading.Event()

    self.observer = Observer()
    for path in self.handlers.keys():
      self.observer.schedule(self.handlers[path], path)
      if not os.path.exists(path):
        os.mkdir(path)

    signal.signal(signal.SIGINT, self.signal_handler)

  def signal_handler(self, signal, frame):
    self.stop()
    sys.exit(0)

  def start(self):
    log.info('"%s" Start watching', list(self.handlers.keys()))
    self.observer.start()
    self.isOldFilesExists()

    while not self.event.is_set():
      self.event.wait(2)

  def isOldFilesExists(self):
    for path in self.handlers.keys():
      oldFiles = os.listdir(path)
      if oldFiles.__len__() > 0:
        log.info('%s Unhandled files detected', path)
        for f in oldFiles:
          workWrapper(self.handlers[path].work, os.path.join(path, f))

  def stop(self):
    log.info('Stop watching...')
    self.observer.stop()
    self.observer.join()
    self.event.set()
