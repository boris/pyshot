import pyinotify
import os
import datetime
import subprocess

wm = pyinotify.WatchManager()
mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        new = datetime.datetime.now().strftime("%s")
        new_name = event.path + "/" + new + ".png"
        os.rename(event.pathname, new_name)
        subprocess.call(['scp', new_name, 'irc.zsh.io:/var/www/html/snap'])


handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('/tmp/screenshots', mask, rec=True)

notifier.loop()
#def main():
#    wm = pyinotify.WatchManager()
#    wm.add_watch('/tmp/screenshots', pyinotify.IN_CREATE, rec=True)
#    notifier = pyinotify.Notifier(wm)
#    message("New File!", "http://www.google.cl")
#    os.system('scp %s irc.zsh.io:/var/www/html/snap' % filename)
#    notifier.loop()
#
#def message(title, message):
#    os.system('notify-send "'+title+'" "'+message+'"')
