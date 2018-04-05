import requests, json, os.path, sys, time
from subprocess import call
from glob import glob
from random import randint

def config_missing():
    print "You must configure the \"server\" parameter in config.py"
    sys.exit(1)


def check_for_command(response, **kwargs):
    global clip_dir, play_cmd
    data = json.loads(response.text)
    print json.dumps(data, indent=2)
    if "clips" in data.keys():
        for clip in data["clips"]:
            print "clip %s command received" % clip
            if os.path.isdir("%s/%s" % (clip_dir, clip)):
                clip_file = "%s/%s/%s.mp3" % (clip_dir, clip, clip)
                if not os.path.exists(clip_file):
                    print "Is directory"
                    clips = glob("%s/%s/%s*.mp3" % (clip_dir, clip, clip))
                    clip_file = clips[randint(0, len(clips)-1)]
                else:
                    print "Is file"
                print "Playing %s" % clip_file
                call([play_cmd, clip_file])
            else:
                print "Couldn't find directory %s/%s" % (clip_dir, clip)


if not os.path.isfile('config.json'):
    config_missing()

config = json.load(open('config.json'))

if not config or "server" not in config.keys():
    config_missing()

server = config["server"]

if "port" in config.keys():
    port = config["port"]
else:
    port = 80

if "client_id" in config.keys():
    client_id = config["client_id"]
else:
    client_id = call(["hostname"])

if "clip_dir" in config.keys():
    clip_dir = config["clip_dir"]
else:
    clip_dir = "/var/www"

if "play_cmd" in config.keys():
    play_cmd = config["play_cmd"]
else:
    play_cmd = "/usr/bin/play"

while True:
    try:
        requests.get("http://%s:%s/cmd/%s" % (server, port, client_id), hooks={'response':check_for_command})
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print e
        time.sleep(5)
