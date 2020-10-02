#!/usr/bin/env PYTHONUNBUFFERED=1 python

import requests, json, sys, time, glob, random
import os
from subprocess import call, check_output
from requests.exceptions import ReadTimeout


checkpoint = 0


def play_speech(text):
    global google_translate_limit, play_cmd, play_options
    parcel_index = 0
    text = text.replace("@COLON@", ":")
    if len(text) > google_translate_limit:
        char_count = 0
        index = 0
        parcel = []
        for word in text.split():
            char_count += len(word) + 1
            if char_count > google_translate_limit:
                get_speech_file(parcel, parcel_index)
                parcel = [word]
                char_count = len(word) + 1
                parcel_index += 1
            else:
                parcel.append(word)
                index += 1
        get_speech_file(parcel, parcel_index)
    else:
        get_speech_file([text], parcel_index)
    call("cat /tmp/speech[0-9]*.mp3 > /tmp/speech.mp3", shell=True)
    call("%s /tmp/speech.mp3 %s" % (play_cmd, play_options), shell=True)
    call("rm -f /tmp/speech*.mp3", shell=True)



def get_speech_file(parcel, parcel_index):
    words = " ".join(parcel)
    headers = { 'User-Agent': 'Mozilla' }
    url = "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=%s&tl=En-us" % words
    filename = "/tmp/speech%s.mp3" % parcel_index
    response = requests.get(url=url, headers=headers, stream=True)
    with open (filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)


def do_command(data):
    global poltergeist_dir, clip_dir, play_cmd, play_unkillable_cmd, quiet_queue, verbosity, checkpoint
    clip_played = False
    if verbosity > 1:
        print(json.dumps(data, indent=2))
    if "clips" in list(data.keys()):
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
                print("Put %s in the queue" % clip)
            else:
                if verbosity > 1:
                    print("clip %s command received" % clip)
                if clip.startswith("speech"):
                    play_speech(" ".join(clip.split()[1:]))
                elif os.path.isdir("%s%s%s" % (clip_dir, os.path.sep, clip)):
                    clip_file = "%s%s%s%s%s.mp3" % (clip_dir, os.path.sep, clip, os.path.sep, clip)
                    if not os.path.exists(clip_file):
                        if verbosity > 1:
                            print("Is directory")
                        clips = glob.glob("%s%s%s%s%s*.mp3" % (clip_dir, os.path.sep, clip, os.path.sep, clip))
                        clip_file = clips[random.randint(0, len(clips)-1)]
                    elif verbosity > 1:
                        print("Is file")
                    if verbosity > 0:
                        print("Playing %s" % clip_file)
                    if clip == "inagaddadavida":
                        actual_play_cmd = play_unkillable_cmd
                    else:
                        actual_play_cmd = play_cmd
                    call("%s %s %s" % (actual_play_cmd, clip_file, play_options), shell=True)
                else:
                    if verbosity > 1:
                        print("Couldn't find directory %s%s%s" % (clip_dir, os.path.sep, clip))
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
                        print("Couldn't find site for clip %s" % clip)


def process_quiet_queue(dummy):
    global clip_dir, quiet_queue, cmd_to_kill, killall_cmd, verbosity
    if verbosity > 1:
        print("Starting up quiet queue")
    try:
        while True:
            while not quiet_queue.empty():
                    if verbosity > 0:
                        print("Killing all sounds")
                    try:
                        clip = quiet_queue.get()
                        if clip == "quiet_all":
                            call(["killall", play_unkillable_cmd])
                        full_kill_cmd = killall_cmd.split(" ")
                        full_kill_cmd.append(cmd_to_kill)
                        call(full_kill_cmd)
                    except OSError as e:
                        # We don't care if the killall command fails
                        print(e)
                        pass
            time.sleep(0.1)
    except Exception as e:
        if verbosity > 0:
            print("Encountered exception in process_quiet_queue:")
            print(e)


def get_config():
    global config_file, config, schema, server, port, client_id, poltergeist_dir, clip_dir, play_cmd, \
            play_unkillable_cmd, cmd_to_kill, killall_cmd, play_options, verbosity, \
            google_translate_limit

    if not config_file:
        if not os.path.isfile('config.json'):
            if sys.platform == "win32":
                appdata_dir = os.getenv('appdata')
                if not os.path.isfile("%s\\.poltergeist\\config.json" % appdata_dir):
                    print("You must configure %%appdata%%\\.poltergeist\\config.py -- see config-dist.json for an example")
                    sys.exit(1)
                else:
                    config_file = "%s\\.poltergeist\\config.json" % appdata_dir
            else:
                home_dir = os.getenv('HOME')
                if not os.path.isfile("%s/.poltergeist/config.json" % home_dir):
                    print("You must configure $HOME/.poltergeist/config.py -- see config-dist.json for an example")
                    sys.exit(1)
                else:
                    config_file = "%s/.poltergeist/config.json" % home_dir
        else:
            config_file = 'config.json'

        print("Using config file %s" % config_file)

    config = json.load(open(config_file))
    schema = config.get("schema", "http")
    server = config.get("server", "localhost")
    port = config.get("port", 80)
    client_id = config.get("client_id", check_output("hostname"))
    poltergeist_dir = config.get("poltergeist_dir", "/root/poltergeist")
    clip_dir = config.get("clip_dir", "/var/www")
    play_cmd = config.get("play_cmd", "/usr/bin/play")
    play_unkillable_cmd = config.get("play_unkillable_cmd", "/usr/bin/play-unkillable")
    play_options = config.get("play_options", "pad 30000s@0:00 >/dev/null 2>&1")
    cmd_to_kill = config.get("cmd_to_kill", config.get("kill_cmd", "play"))
    killall_cmd = config.get("killall_cmd", "killall")
    verbosity = int(config.get("verbosity", 1))
    google_translate_limit = int(config.get("google_translate_limit", 100))
    if config.get("debug"):
        verbosity = 2
    if config.get("quiet"):
        verbosity = 0

config_file = None
get_config()
if sys.version_info[0] >= 3:
    import _thread, queue
    quiet_queue = queue.Queue()
    _thread.start_new_thread(process_quiet_queue, (None,))
else:
    import thread, Queue
    quiet_queue = Queue.Queue()
    thread.start_new_thread(process_quiet_queue, (None,))
if verbosity > 0:
    print("Verbosity set to %s" % verbosity)

while True:
    try:
        get_config()
        if verbosity > 0:
            print("Connecting to %s on port %s as client_id %s" % (server, port, client_id))
        r = requests.get("%s://%s:%s/cmd/%s" % (schema, server, port, client_id), stream=True, timeout=600)
        if verbosity > 0:
            print("Received bytes from server")
        for json_data in r.iter_lines():
            if json_data:
                if sys.version_info[0] >= 3:
                    _thread.start_new_thread(do_command, (json.loads(json_data),))
                else:
                    thread.start_new_thread(do_command, (json.loads(json_data),))
    except ReadTimeout:
        # The connection is designed to timeout and refresh every 10 minutes
        if verbosity > 1:
            print("Didn't receive a command in 10 minutes. Looping.")
    except KeyboardInterrupt:
        if verbosity > 0:
            print("Received CTRL-C, exiting...")
        sys.exit(0)
    except Exception as e:
        if verbosity > 0:
            print("Received unexpected exception:")
            print(e)
            print("Reconnecting in 5 seconds...")
        time.sleep(5)
