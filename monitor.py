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

        # S3 upload
        session = boto3.Session(profile_name='boris')
        s3_client = session.client('s3')
        s3_client.upload_file(new_name, 
                'imgs.zsh.io', 
                new_name[17:],
                ExtraArgs={'ContentType': 'image/png'})
        os.remove(new_name)

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('/tmp/screenshots', mask, rec=True)

notifier.loop()
