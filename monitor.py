import pyinotify
import os
import datetime
import subprocess
import boto3

wm = pyinotify.WatchManager()
mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE

if not os.path.exists("~/Pictures/Screenshots/"):
    os.makedirs("~/Pictures/Screenshots/")

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print("Creating:", event.pathname)
        new = datetime.datetime.now().strftime("%s")
        new_name = event.path + "/" + new + ".png"
        os.rename(event.pathname, new_name)
        subprocess.call(f"aws s3 cp {new_name} s3://borisquiroz.dev", shell=True)
        print(f"Uploaded to S3: {new_name}")
        os.remove(new_name)

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('~/Pictures/Screenshots', mask, rec=True)

notifier.loop()
