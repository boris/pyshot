import pyinotify, os, datetime, subprocess

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
