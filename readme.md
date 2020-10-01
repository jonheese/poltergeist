# Poltergeist
Makes TVs (and other computers) talk to you

Poltergeist uses a server/client architecture, where there is a single server to which clients connect and subscribe to sound clip events from a queue.  You probably want to run a client (runs on your local machine, waits for sound clip events and plays the sound clips for you).

## Client Installation
### Linux (Ubuntu 18.04+ or RHEL/CentOS 7+ or Fedora or Raspbian (with systemd))
```
cd poltergeist/client
mkdir ~/.poltergeist
cp config-dist.json ~/.poltergeist/config.json
# edit ~/.poltergeist/config.json, filling in the appropriate values, here are some suggestions:
#
#    "client_id": "inetu-hdmi19",
#    "poltergeist_dir": "/path/to/poltergeist",
#    "clip_dir": "/path/to/poltergeist/webdirs",
#    "play_cmd": "/usr/bin/play",
#    "play_unkillable_cmd": "/usr/bin/play",
#    "play_options": "pad 30000s@0:00 >/dev/null 2>&1",
#    "kill_cmd": "play",
#    "killall_cmd": "killall",
#    "debug": false,
#    "quiet": true
#
./install-client.sh # provide sudo password
systemctl start poltergeist-client
```
To uninstall:
```
./uninstall-client.sh # provide sudo password
```

### MacOS
```
cd poltergeist/client
mkdir ~/.poltergeist
cp config-dist.json ~/.poltergeist/config.json
# edit ~/.poltergeist/config.json, filling in the appropriate values, here are some suggestions:
#
#    "client_id": "inetu-hdmi19",
#    "poltergeist_dir": "/path/to/poltergeist",
#    "clip_dir": "/path/to/poltergeist/webdirs",
#    "play_cmd": "/usr/bin/afplay",
#    "play_unkillable_cmd": "/usr/bin/afplay",
#    "play_options": ">/dev/null 2>&1",
#    "kill_cmd": "afplay",
#    "killall_cmd": "killall",
#    "debug": false,
#    "quiet": true
#
./install-client.sh # provide sudo password
lanchctl load /Library/LaunchAgents/com.jonheese.poltergeist-client.plist
```
To uninstall:
```
./uninstall-client.sh # provide sudo password
```

### Windows
NOTE: You will need to install Python and add its bin directory to your `%PATH%` before any of this will work on Windows.

NOTE: You will also need to install the `requests` Python.  This can usually be done by running
```pip.exe install -y requests```

NOTE: Due to the way that Windows services interact with audio devices, the Windows client is simply run in the background and must be manually stopped.  Scripts are provided to do this, and the starting can be automated using Windows startup features. 
```
cd poltergeist\client
mkdir %appdata%\.poltergeist
cp config-dist.json %appdata%\.poltergeist\config.json
# edit %appdata%\.poltergeist\config.json, filling in the appropriate values, here are some suggestions:
#
#    "client_id": "inetu-hdmi19",
#    "poltergeist_dir": "c:\\Path\\to\\poltergeist",
#    "clip_dir": "c:\\Path\\to\\poltergeist\\webdirs",
#    "play_cmd": "c:\\Path\\to\\poltergeist\\tools\\cmdmp3win.exe",
#    "play_unkillable_cmd": "c:\\Path\\to\\poltergeist\\tools\\cmdmp3win.exe",
#    "kill_cmd": "cmdmp3win.exe",
#    "killall_cmd": "c:\\Windows\\system32\\taskkill.exe -F -T -IM",
#    "play_options": "",
#    "debug": false,
#    "quiet": true
#
# edit start-poltergeist.ps1 and fill in the path to the pythonw.exe binary on your system
```

#### Starting the Poltergeist client
```
.\start-poltergeist.ps1
```

#### Stopping the Poltergeist client:
```
.\stop-poltergeist.ps1
```

## Keeping your content updated
It is recommended that you schedule `git pull`s on a regular basis (via `cron` or Task Scheduled) to ensure that you have the latest sound clip files.  This is left as an exercise for the reader.

## Adding your own content
### Using the automatic deploy script (`addsite.sh`)
1. Check out this project:
    ```
    $ git clone <clone_url>
    ```
2. Copy your desired mp3 file, named `<sitename>.mp3`, to the `webdirs` directory:
    ```
    $ cp <sitename>.mp3 webdirs/
    ```
3. **Optional:** Copy a `jpg`/`png` file, named `<sitename>.[jpg|png]`, to the `webdirs` directory, if you want an image to display on the page:
    ```
    $ cp <sitename>.png webdirs/
    ```
4. Run the addsite.sh script:
    ```
    $ ./addsite.sh
    Enter site name: <sitename>
    Enter page title: New Title!
    Do you have any customizations to make before commit/push/deploy? [y/N]:
    ```
5. If you want to make any further customizations to make before committing (eg. any special logic in the `index.php` or something), enter `y`, make those changes, then commit, push, deploy (see below).
6. If you have no further customizations to make, enter `n` and the script will automatically add, commit, and push.

### Manual Deploy Steps ###
If you had additional customizations to be made before committing in the steps above, you can commit, push, and deploy with the following commands:
```
git add .
git commit -a
git push -u origin
```
