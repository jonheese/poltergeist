# Poltergeist
Makes TVs (and other computers) talk to you

Poltergeist uses a server/client architecture, where there is a single server to which clients connect and subscribe to sound clip events from a queue.  You probably want to run a client (runs on your local machine, waits for sound clip events and plays the sound clips for you).

NOTE: Poltergeist can run on Python 2.7 or 3.x, although 3.x is preferred and support for 2.7 will be deprecated at some point in the future.

## Client Installation
### Arming/Disarming Time
The settings `arm_time` and `disarm_time` are optional and tell the Poltergeist client when you want sound clips to be played.  If you do not specify either of them, sound clips will be played 24x7 on demand.  If you specify _either_ of them, sound clips will only be played after the `arm_time` and before the `disarm_time`, with the default value for `arm_time` being `7:00` and `disarm_time` being `17:00`.

### Blacklist
The optional setting `blacklist` is a list of clip names that will never be played on your Poltergeist client.  If not present (or empty) all available clips will be played as normal.  If a blacklisted clip is requested in your Poltergeist client it will be ignored. 

### Linux
Should work on Ubuntu 18.04+, Debian 8+, RHEL/CentOS 7+, Fedora, or Raspbian (really, any Linux with systemd and either `yum` or `apt`).
```
cd poltergeist/client
mkdir ~/.poltergeist
cp config-dist.json ~/.poltergeist/config.json
# edit ~/.poltergeist/config.json, filling in the appropriate values, here are some suggestions:
#
#    "schema" : "http",
#    "server" : "your.poltergeist.server.com",
#    "port": 80,
#    "client_id": "inetu-hdmi19",
#    "poltergeist_dir": "/path/to/poltergeist",
#    "clip_dir": "/path/to/poltergeist/webdirs",
#    "play_cmd": "/usr/bin/play",
#    "play_unkillable_cmd": "/usr/bin/play",
#    "play_options": "pad 30000s@0:00 >/dev/null 2>&1",
#    "killall_cmd": "killall",
#    "cmd_to_kill": "play",
#    "debug": false,
#    "quiet": true,
#    "arm_time": "7:00",
#    "disarm_time": "17:00",
#    "blacklist": [
#        "lastchristmas"
#    ]
#
./install-client.sh # provide sudo password, if not root
systemctl start poltergeist-client
```
To uninstall:
```
./uninstall-client.sh # provide sudo password, if not root
```

### MacOS
```
cd poltergeist/client
mkdir ~/.poltergeist
cp config-dist.json ~/.poltergeist/config.json
# edit ~/.poltergeist/config.json, filling in the appropriate values, here are some suggestions:
#
#    "schema" : "http",
#    "server" : "your.poltergeist.server.com",
#    "port": 80,
#    "client_id": "inetu-hdmi19",
#    "poltergeist_dir": "/path/to/poltergeist",
#    "clip_dir": "/path/to/poltergeist/webdirs",
#    "play_cmd": "/usr/bin/afplay",
#    "play_unkillable_cmd": "/usr/bin/afplay",
#    "play_options": ">/dev/null 2>&1",
#    "killall_cmd": "killall",
#    "cmd_to_kill": "afplay",
#    "debug": false,
#    "quiet": true,
#    "arm_time": "7:00",
#    "disarm_time": "17:00",
#    "blacklist": [
#        "lastchristmas"
#    ]
#
./install-client.sh # provide sudo password, if not root
lanchctl load /Library/LaunchAgents/com.jonheese.poltergeist-client.plist
```
To uninstall:
```
./uninstall-client.sh # provide sudo password, if not root
```

### Windows
NOTE: You will need to install Python 3.x and add its bin directory to your `%PATH%` before any of this will work on Windows.

NOTE: You will also need to install the `requests` Python package.  This can usually be done by running
```pip.exe install -y requests```

NOTE: Due to the way that Windows services interact with audio devices (read: poorly, if at all), the Windows client is simply run as a standard background processd and must be manually stopped.  Scripts are provided to do this, and the starting can be automated using Windows startup features. 
```
cd poltergeist\client
mkdir %appdata%\.poltergeist
cp config-dist.json %appdata%\.poltergeist\config.json
# edit %appdata%\.poltergeist\config.json, filling in the appropriate values, here are some suggestions:
#
#    "schema" : "http",
#    "server" : "your.poltergeist.server.com",
#    "port": 80,
#    "client_id": "inetu-hdmi19",
#    "poltergeist_dir": "c:\\Path\\to\\poltergeist",
#    "clip_dir": "c:\\Path\\to\\poltergeist\\webdirs",
#    "play_cmd": "c:\\Path\\to\\poltergeist\\tools\\cmdmp3win.exe",
#    "play_unkillable_cmd": "c:\\Path\\to\\poltergeist\\tools\\cmdmp3win.exe",
#    "killall_cmd": "c:\\Windows\\system32\\taskkill.exe -F -T -IM",
#    "cmd_to_kill": "cmdmp3win.exe",
#    "play_options": "",
#    "debug": false,
#    "quiet": true,
#    "arm_time": "7:00",
#    "disarm_time": "17:00",
#    "blacklist": [
#        "lastchristmas"
#    ]
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
It is recommended that you schedule `git pull`s on a regular basis (via `cron` or Task Scheduler) to ensure that you have the latest sound clip files.  This is left as an exercise for the reader.

## Adding your own content
### Using the automatic server deploy script (`addsite.sh`)
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

### Manual Server Deploy Steps ###
If you had additional customizations to be made before committing in the steps above, you can commit, push, and deploy with the following commands:
```
git add .
git commit -a
git push -u origin
```
