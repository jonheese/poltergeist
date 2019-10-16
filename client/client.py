import requests, json, os.path, sys, time, thread, Queue, glob, random
from subprocess import call, check_output
from requests.exceptions import ReadTimeout


checkpoint = 0


def do_command(data):
    global clip_dir, play_cmd, play_unkillable_cmd, quiet_queue, verbosity, checkpoint
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
                if os.path.isdir("%s/%s" % (clip_dir, clip)):
                    clip_file = "%s/%s/%s.mp3" % (clip_dir, clip, clip)
                    if not os.path.exists(clip_file):
                        if verbosity > 1:
                            print "Is directory"
                        clips = glob.glob("%s/%s/%s*.mp3" % (clip_dir, clip, clip))
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
                        print "Couldn't find directory %s/%s" % (clip_dir, clip)
                    for file_name in glob.glob("/etc/apache2/sites-enabled/*.conf"):
                        with open(file_name) as f:
                            contents = f.read()
                        for line in contents.splitlines():
                            if 'ServerAlias' in line:
                                alias = line.split(" ")[1]
                                if alias.split(".")[0] == clip:
                                    actual_clip = file_name.split("/")[-1].split(".")[0]
                                    clip_file = "%s/%s/%s.mp3" % (clip_dir, actual_clip, actual_clip)
                                    call("%s %s %s" % (play_cmd, clip_file, play_options), shell=True)
                                    clip_played = True
                                    break
                    if not clip_played:
                        print "Couldn't find site for clip %s" % clip


def process_quiet_queue(dummy):
    global clip_dir, quiet_queue, verbosity
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
                        kill_cmd = play_cmd.split("/")[-1]
                        print "killall %s" % kill_cmd
                        call(["killall", kill_cmd])
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
    if not os.path.isfile('config.json'):
        print "You must configure config.py -- see config-dist.json for an example"
        sys.exit(1)

    global config, schema, server, port, client_id, clip_dir, play_cmd, play_unkillable_cmd, play_options, verbosity
    config = json.load(open('config.json'))
    schema = config["schema"] if "schema" in config.keys() else "http"
    server = config["server"] if "server" in config.keys() else "localhost"
    port = config["port"] if "port" in config.keys() else 80
    client_id = config["client_id"] if "client_id" in config else check_output("hostname")
    clip_dir = config["clip_dir"] if "clip_dir" in config.keys() else "/var/www"
    play_cmd = config["play_cmd"] if "play_cmd" in config.keys() else "/usr/bin/play"
    play_unkillable_cmd = config["play_unkillable_cmd"] if "play_unkillable_cmd" in config.keys() else "/usr/bin/play-unkillable"
    play_options = config["play_options"] if "play_options" in config.keys() else "pad 30000s@0:00"
    verbosity = int(config["verbosity"]) if "verbosity" in config.keys() else 1
    if "debug" in config.keys() and bool(config["debug"]):
        verbosity = 2
    if "quiet" in config.keys() and bool(config["quiet"]):
        verbosity = 0


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
