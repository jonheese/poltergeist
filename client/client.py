import requests, json, os.path, sys, time, thread, Queue, glob, random
from subprocess import call, check_output
from requests.exceptions import ReadTimeout


checkpoint = 0


def do_command(data):
    global poltergeist_dir, clip_dir, play_cmd, play_unkillable_cmd, quiet_queue, verbosity, checkpoint
    clip_played = False
    if verbosity > 1:
        print json.dumps(data, indent=2)
    if "clips" in data.keys():
        for clip in data["clips"]:
            timestamp = float(clip.split(":")[1])
            if timestamp <= checkpoint:
                if timestamp + 60 <= time.time():
                    requests.get("%s://%s:%s/delete/poltergeist:clip:%s:%s" % (schema, server, port, client_id, timestamp))
                continue
            if timestamp > checkpoint:
                checkpoint = timestamp
            clip = clip.split(":")[0]
            if clip == "quiet" or clip == "quiet_all":
                quiet_queue.put(clip)
                print "Put %s in the queue" % clip
            else:
                if verbosity > 1:
                    print "clip %s command received" % clip
                if os.path.isdir("%s%s%s" % (clip_dir, os.path.sep, clip)):
                    clip_file = "%s%s%s%s%s.mp3" % (clip_dir, os.path.sep, clip, os.path.sep, clip)
                    if not os.path.exists(clip_file):
                        if verbosity > 1:
                            print "Is directory"
                        clips = glob.glob("%s%s%s%s%s*.mp3" % (clip_dir, os.path.sep, clip, os.path.sep, clip))
                        clip_file = clips[random.randint(0, len(clips)-1)]
                    elif verbosity > 1:
                        print "Is file"
                    if verbosity > 0:
                        print "Playing %s" % clip_file
                    if clip == "inagaddadavida":
                        actual_play_cmd = play_unkillable_cmd
                    else:
                        actual_play_cmd = play_cmd
                    call("%s %s %s" % (actual_play_cmd, clip_file, play_options), shell=True)
                else:
                    if verbosity > 1:
                        print "Couldn't find directory %s%s%s" % (clip_dir, os.path.sep, clip)
                    for file_name in glob.glob("%s%sapache-confs%s*.conf" % (poltergeist_dir, os.path.sep, os.path.sep)):
                        with open(file_name) as f:
                            contents = f.read()
                        for line in contents.splitlines():
                            if 'ServerAlias' in line:
                                alias = line.split(" ")[1]
                                if alias.split(".")[0] == clip:
                                    actual_clip = file_name.split(os.path.sep)[-1].split(".")[0]
                                    clip_file = "%s%s%s%s%s.mp3" % (clip_dir, os.path.sep, actual_clip, os.path.sep, actual_clip)
                                    call("%s %s %s" % (play_cmd, clip_file, play_options), shell=True)
                                    clip_played = True
                                    break
                    if not clip_played:
                        print "Couldn't find site for clip %s" % clip


def process_quiet_queue(dummy):
    global clip_dir, quiet_queue, kill_cmd, killall_cmd, verbosity
    if verbosity > 1:
        print "Starting up quiet queue"
    try:
        while True:
            while not quiet_queue.empty():
                    if verbosity > 0:
                        print "Killing all sounds"
                    try:
                        clip = quiet_queue.get()
                        if clip == "quiet_all":
                            call(["killall", play_unkillable_cmd])
                        full_kill_cmd = killall_cmd.split(" ")
                        full_kill_cmd.append(kill_cmd)
                        call(full_kill_cmd)
                    except OSError as e:
                        # We don't care if the killall command fails
                        print e
                        pass
            time.sleep(0.1)
    except Exception as e:
        if verbosity > 0:
            print "Encountered exception in process_quiet_queue:"
            print e


def get_config():
    global config_file, config, schema, server, port, client_id, poltergeist_dir, clip_dir, play_cmd, \
            play_unkillable_cmd, kill_cmd, killall_cmd, play_options, verbosity

    if not config_file:
        if not os.path.isfile('config.json'):
            if sys.platform == "win32":
                appdata_dir = os.getenv('appdata')
                if not os.path.isfile("%s\\.poltergeist\\config.json" % appdata_dir):
                    print "You must configure %%appdata%%\\.poltergeist\\config.py -- see config-dist.json for an example"
                    sys.exit(1)
                else:
                    config_file = "%s\\.poltergeist\\config.json" % appdata_dir
            else:
                home_dir = os.getenv('HOME')
                if not os.path.isfile("%s/.poltergeist/config.json" % home_dir):
                    print "You must configure $HOME/.poltergeist/config.py -- see config-dist.json for an example"
                    sys.exit(1)
                else:
                    config_file = "%s/.poltergeist/config.json" % home_dir
        else:
            config_file = 'config.json'

        print "Using config file %s" % config_file

    config = json.load(open(config_file))
    schema = config["schema"] if "schema" in config.keys() else "http"
    server = config["server"] if "server" in config.keys() else "localhost"
    port = config["port"] if "port" in config.keys() else 80
    client_id = config["client_id"] if "client_id" in config else check_output("hostname")
    poltergeist_dir = config["poltergeist_dir"] if "poltergeist_dir" in config.keys() else "/root/poltergeist"
    clip_dir = config["clip_dir"] if "clip_dir" in config.keys() else "/var/www"
    play_cmd = config["play_cmd"] if "play_cmd" in config.keys() else "/usr/bin/play"
    play_unkillable_cmd = config["play_unkillable_cmd"] if "play_unkillable_cmd" in config.keys() else "/usr/bin/play-unkillable"
    play_options = config["play_options"] if "play_options" in config.keys() else "pad 30000s@0:00 >/dev/null 2>&1"
    kill_cmd = config["kill_cmd"] if "kill_cmd" in config.keys() else "play"
    killall_cmd = config["killall_cmd"] if "killall_cmd" in config.keys() else "killall"
    verbosity = int(config["verbosity"]) if "verbosity" in config.keys() else 1
    if "debug" in config.keys() and bool(config["debug"]):
        verbosity = 2
    if "quiet" in config.keys() and bool(config["quiet"]):
        verbosity = 0

config_file = None
get_config()
quiet_queue = Queue.Queue()
thread.start_new_thread(process_quiet_queue, (None,))
if verbosity > 0:
    print "Verbosity set to %s" % verbosity

while True:
    try:
        get_config()
        if verbosity > 0:
            print "Connecting to %s on port %s as client_id %s" % (server, port, client_id)
        r = requests.get("%s://%s:%s/cmd/%s" % (schema, server, port, client_id), stream=True, timeout=600)
        if verbosity > 0:
            print "Received bytes from server"
        for json_data in r.iter_lines():
            if json_data:
                thread.start_new_thread(do_command, (json.loads(json_data),))
    except ReadTimeout:
        # The connection is designed to timeout and refresh every 10 minutes
        if verbosity > 1:
            print "Didn't receive a command in 10 minutes. Looping."
    except KeyboardInterrupt:
        if verbosity > 0:
            print "Received CTRL-C, exiting..."
        sys.exit(0)
    except Exception as e:
        if verbosity > 0:
            print "Received unexpected exception:"
            print e
            print "Reconnecting in 5 seconds..."
        time.sleep(5)
