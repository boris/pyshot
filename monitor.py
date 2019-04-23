import pyinotify, os, datetime, subprocess
import clipboard

wm = pyinotify.WatchManager()
mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE

if not os.path.exists("/tmp/screenshots/"):
    os.makedirs("/tmp/screenshots/")

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        new = datetime.datetime.now().strftime("%s")
        new_name = event.path + "/" + new + ".png"
        os.rename(event.pathname, new_name)
        # Needs to be fixed!
        #url = "http://irc.zsh.io:8080/ss/" + new + ".png"
        #clipboard.copy(url)
        subprocess.call(['scp', new_name, 'moby:apps/screenshots/imgs'])
        notify = "notify-send 'https://imgs.zsh.io/{}.png'".format(new)
        os.system(notify)
        os.remove(new_name)

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('/tmp/screenshots', mask, rec=True)

notifier.loop()
