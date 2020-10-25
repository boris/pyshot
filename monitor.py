import pyinotify
import os
import datetime
import subprocess
import boto3

wm = pyinotify.WatchManager()
mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE

if not os.path.exists("/tmp/screenshots/"):
    os.makedirs("/tmp/screenshots/")

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        new = datetime.datetime.now().strftime("%s")
        new_name = event.path + "/" + new + ".png"
        os.rename(event.pathname, new_name)
        subprocess.call('scp -i ~/.ssh/keys/id_rsa_pyshot {} jumphost-aws:~/shots'.format(new_name), shell=True)
        os.remove(new_name)

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('/tmp/screenshots', mask, rec=True)

notifier.loop()
