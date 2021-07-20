# import time module, Observer, FileSystemEventHandler
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os


# -This file is used to monitor the directory where we store the DBF files.
# -When a change is made to the database, the file sync software we have implemented replaces the old DBF file with a new one.
# -When the file is replaced, this script then triggers the transact.py and maxride.py scripts to update the database.
# *! NOTE: The replacement of DBF files does not automatically trigger this script(monitor.py), you must have it running for it to work

#adding PID file for monit watchdog checking

outputfile = open('/tmp/monitorpy.pid', "w")
pid = str(os.getpid())
outputfile.write(pid)
outputfile.close()

  
class OnMyWatch:
    # Set the directory on watch
    watchDirectory = "/var/sftp/eoc"
    #watchDirectory = "/var/www/html/eoc/audio"
  
    def __init__(self):
        self.observer = Observer()
  
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
  
        self.observer.join()
  
  
class Handler(FileSystemEventHandler):
  
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
  
        elif event.event_type == 'created':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)
            try:
                os.system("python3 /var/www/html/eoc/scripts/maxride.py")
            except Exception as e:
                print(e)
            try:        
               os.system("python3 /var/www/html/eoc/scripts/transact.py")
            except Exception as e:
                print(e)
            
              
if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()
