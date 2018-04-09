import requests, json, os.path, sys, time, thread, Queue, glob, random
from subprocess import call, check_output


def do_command(data):
    global clip_dir, play_cmd, quiet_queue, debug, quiet
    if debug:
        print json.dumps(data, indent=2)
    if "clips" in data.keys():
        for clip in data["clips"]:
            if clip == "quiet":
                quiet_queue.put(clip)
                print "Put %s in the queue" % clip
            else:
                if debug:
                    print "clip %s command received" % clip
                if os.path.isdir("%s/%s" % (clip_dir, clip)):
                    clip_file = "%s/%s/%s.mp3" % (clip_dir, clip, clip)
                    if not os.path.exists(clip_file):
                        if debug:
                            print "Is directory"
                        clips = glob.glob("%s/%s/%s*.mp3" % (clip_dir, clip, clip))
                        clip_file = clips[random.randint(0, len(clips)-1)]
                    elif debug:
                        print "Is file"
                    if not quiet:
                        print "Playing %s" % clip_file
                    call("%s %s %s >/dev/null 2>&1" % (play_cmd, clip_file, play_options), shell=True)
                elif debug:
                    print "Couldn't find directory %s/%s" % (clip_dir, clip)


def process_quiet_queue(dummy):
    global clip_dir, play_cmd, quiet_queue, debug, quiet
    try:
        while True:
            while not quiet_queue.empty():
                    if not quiet:
                        print "Killing all sounds"
                    try:
                        call(["killall", "play"])
                        quiet_queue.get()
                    except OSError as e:
                        # We don't care if the killall command fails
                        print e
                        pass
            time.sleep(0.1)
    except Exception as e:
        if not quiet:
            print "Encountered exception in process_quiet_queue:"
            print e


if not os.path.isfile('config.json'):
    print "You must configure config.py -- see config-dist.json for an example"
    sys.exit(1)

config = json.load(open('config.json'))
server = config["server"] if "server" in config.keys() else "localhost"
port = config["port"] if "port" in config.keys() else 80
client_id = config["client_id"] if "client_id" in config else check_output("hostname")
clip_dir = config["clip_dir"] if "clip_dir" in config.keys() else "/var/www"
play_cmd = config["play_cmd"] if "play_cmd" in config.keys() else "/usr/bin/play"
play_options = config["play_options"] if "play_options" in config.keys() else "pad 30000s@0:00"
debug = bool(config["debug"]) if "debug" in config.keys() else False
quiet = bool(config["quiet"]) if "quiet" in config.keys() else False

quiet_queue = Queue.Queue()
thread.start_new_thread(process_quiet_queue, (None,))

while True:
    try:
        if not quiet:
            print "Connecting to %s on port %s as client_id %s" % (server, port, client_id)
        r = requests.get("http://%s:%s/cmd/%s" % (server, port, client_id), stream=True)
        for json_data in r.iter_lines():
            if json_data:
                print json.dumps(json.loads(json_data), indent=2)
                thread.start_new_thread(do_command, (json.loads(json_data),))
    except KeyboardInterrupt:
        if not quiet:
            print "Received CTRL-C, exiting..."
        sys.exit(0)
    except Exception as e:
        if not quiet:
            print "Received unexpected exception:"
            print e
            print "Reconnecting in 5 seconds..."
        time.sleep(5)
