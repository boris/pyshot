# Py[thon Screen]shot
Motivation: I need to learn python, so in my first week started with a small
project that I already did in Ruby: A script to upload screenshots from
`/tmp/screenshots` to some public location (i.e. one of my servers).

**Setup**
```
sudo pip install pyinotify
# edit pyshot.service, change path
sudo cp pyshot.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable pyshot.service
sudo systemctl start pyshot.service
```

**To Do**
- Daemonize (currently using systemd)
- Copy link to clipboard (xsel ?)
- Show notification on Ubuntu notification
- Make it a module?
