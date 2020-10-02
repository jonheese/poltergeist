#!/usr/bin/env PYTHONUNBUFFERED=1 python

import glob
import json
import logging
import os
import random
import requests
import sys
import time
from subprocess import call, check_output
from requests.exceptions import ReadTimeout


class PoltergeistClient():
    def __init__(self):
        self._log = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%m-%d %H:%M',
        )
        self._log.setLevel(logging.DEBUG)
        self.checkpoint = 0
        self.config_file = None
        self.__get_config()

    def __get_config(self):
        if not self.config_file:
            if not os.path.isfile('config.json'):
                if sys.platform == "win32":
                    appdata_dir = os.getenv('appdata')
                    if not os.path.isfile("%s\\.poltergeist\\config.json" %
                                          appdata_dir):
                        self._log.error("You must configure %%appdata%%\\" +
                                        ".poltergeist\\config.json -- see " +
                                        "config-dist.json for an example")
                        sys.exit(1)
                    else:
                        self.config_file = "%s\\.poltergeist\\config.json" % \
                            appdata_dir
                else:
                    home_dir = os.getenv('HOME')
                    if not os.path.isfile("%s/.poltergeist/config.json" %
                                          home_dir):
                        self._log.error("You must configure $HOME/" +
                                        ".poltergeist/config.json -- see " +
                                        "config-dist.json for an example")
                        sys.exit(1)
                    else:
                        self.config_file = "%s/.poltergeist/config.json" % \
                            home_dir
            else:
                self.config_file = 'config.json'

        self._log.info("Using config file %s" % self.config_file)

        config = json.load(open(self.config_file))
        self.schema = config.get("schema", "http")
        self.server = config.get("server", "localhost")
        self.port = config.get("port", 80)
        self.client_id = config.get("client_id", check_output("hostname"))
        self.poltergeist_dir = config.get(
                                    "poltergeist_dir",
                                    "/root/poltergeist"
                               )
        self.clip_dir = config.get("clip_dir", "/var/www")
        self.play_cmd = config.get("play_cmd", "/usr/bin/play")
        self.play_unkillable_cmd = config.get(
                                        "play_unkillable_cmd",
                                        "/usr/bin/play-unkillable"
                                   )
        self.play_options = config.get(
                                "play_options",
                                "pad 30000s@0:00 >/dev/null 2>&1"
                            )
        self.cmd_to_kill = config.get(
                                "cmd_to_kill",
                                config.get(
                                    "kill_cmd",
                                    "play"
                                )
                           )
        self.killall_cmd = config.get("killall_cmd", "killall")
        verbosity = int(config.get("verbosity", 1))
        self.google_translate_limit = int(config.get(
                                        "google_translate_limit",
                                        100
                                      ))
        if config.get("debug"):
            verbosity = 2
        if config.get("quiet"):
            verbosity = 0

        if verbosity == 0:
            self._log.setLevel(logging.ERROR)
        elif verbosity == 1:
            self._log.setLevel(logging.INFO)
        elif verbosity == 2:
            self._log.setLevel(logging.DEBUG)

        if sys.version_info[0] >= 3:
            import queue
            self.quiet_queue = queue.Queue()
        else:
            import Queue
            self.quiet_queue = Queue.Queue()
        self._log.info("Verbosity set to %s" % verbosity)

    def __start_quiet_queue(self):
        if sys.version_info[0] >= 3:
            import _thread
            _thread.start_new_thread(self.__process_quiet_queue, (None,))
        else:
            import thread
            thread.start_new_thread(self.__process_quiet_queue, (None,))

    def start(self):
        self.__start_quiet_queue()
        while True:
            try:
                self.__get_config()
                self._log.debug(
                    "Connecting to %s on " % self.server +
                    "port %s as client_id %s" % (
                        self.port,
                        self.client_id,
                    )
                )
                r = requests.get(
                    "%s://%s:%s/cmd/%s" % (
                        self.schema,
                        self.server,
                        self.port,
                        self.client_id,
                    ),
                    stream=True, timeout=600
                )
                self._log.info("Received bytes from server")
                for json_data in r.iter_lines():
                    if json_data:
                        if sys.version_info[0] >= 3:
                            import _thread
                            _thread.start_new_thread(
                                self.__do_command,
                                (
                                    json.loads(json_data),
                                )
                            )
                        else:
                            import thread
                            thread.start_new_thread(
                                self.__do_command,
                                (
                                    json.loads(json_data),
                                )
                            )
            except ReadTimeout:
                # The connection is designed to timeout and refresh every 10m
                self._log.debug(
                    "Didn't receive a command in 10 minutes. Looping."
                )
            except KeyboardInterrupt:
                self._log.info("Received CTRL-C, exiting...")
                sys.exit(0)
            except Exception as e:
                self._log.info("Received unexpected exception:")
                self._log.info(e)
                self._log.info("Reconnecting in 5 seconds...")
                time.sleep(5)

    def __process_quiet_queue(self, dummy):
        self._log.debug("Starting up quiet queue")
        try:
            while True:
                while not self.quiet_queue.empty():
                    self._log.info("Killing all sounds")
                    try:
                        clip = self.quiet_queue.get()
                        if clip == "quiet_all":
                            call(["killall", self.play_unkillable_cmd])
                        full_kill_cmd = self.killall_cmd.split(" ")
                        full_kill_cmd.append(self.cmd_to_kill)
                        call(full_kill_cmd)
                    except OSError as e:
                        # We don't care if the killall command fails
                        self._log.error(e)
                        pass
                time.sleep(0.1)
        except Exception as e:
            self._log.info("Encountered exception in process_quiet_queue:")
            self._log.info(e)

    def __handle_clip_lifetime(self, clip):
        timestamp = float(clip.split(":")[1])
        if timestamp <= self.checkpoint:
            if timestamp + 30 <= time.time():
                requests.get(
                    "%s://%s:%s/delete/poltergeist:clip:%s:%s" %
                    (
                        self.schema,
                        self.server,
                        self.port,
                        self.client_id,
                        timestamp
                    )
                )
            return True
        if timestamp > self.checkpoint:
            self.checkpoint = timestamp
        return False

    def __do_command(self, data):
        clip_played = False
        self._log.debug(json.dumps(data, indent=2))
        if "clips" in list(data.keys()):
            for clip in data["clips"]:
                if self.__handle_clip_lifetime(clip):
                    clip_played = True
                    self._log.debug(
                        "Skipping clip %s because it already played" % clip
                    )
                    continue
                clip = clip.split(":")[0]
                if clip == "quiet" or clip == "quiet_all":
                    self.quiet_queue.put(clip)
                    self._log.info("Put %s in the queue" % clip)
                else:
                    self._log.debug("clip %s command received" % clip)
                    if clip.startswith("speech"):
                        clip_played = self.__play_speech(
                            " ".join(clip.split()[1:])
                        )
                    else:
                        clip_played = self.__play_clip(clip)
            if not clip_played:
                self._log.error(
                    "Couldn't find site for clip %s" % clip
                )

    def __play_clip(self, clip):
        if os.path.isdir(
                "%s%s%s" % (
                    self.clip_dir,
                    os.path.sep,
                    clip,
                )):
            clip_file = "%s%s%s%s%s.mp3" % (
                self.clip_dir,
                os.path.sep,
                clip,
                os.path.sep,
                clip
            )
            if not os.path.exists(clip_file):
                self._log.debug("Is directory")
                clips = glob.glob(
                    "%s%s%s%s%s*.mp3" % (
                        self.clip_dir,
                        os.path.sep,
                        clip, os.path.sep,
                        clip
                    )
                )
                clip_file = clips[random.randint(0, len(clips)-1)]
            self._log.debug("Is file")
            self._log.info("Playing %s" % clip_file)
            if clip == "inagaddadavida":
                actual_play_cmd = self.play_unkillable_cmd
            else:
                actual_play_cmd = self.play_cmd
            call(
                "%s %s %s" % (
                    actual_play_cmd,
                    clip_file,
                    self.play_options
                ),
                shell=True
            )
        else:
            self._log.debug(
                "Couldn't find directory %s%s%s" %
                (self.clip_dir, os.path.sep, clip)
            )
            for file_name in glob.glob(
                    "%s%sapache-confs%s*.conf" %
                    (
                        self.poltergeist_dir,
                        os.path.sep,
                        os.path.sep
                    )):
                with open(file_name) as f:
                    contents = f.read()
                for line in contents.splitlines():
                    if 'ServerAlias' in line:
                        alias = line.split(" ")[1]
                        if alias.split(".")[0] == clip:
                            actual_clip = file_name.split(
                                os.path.sep
                            )[-1].split(".")[0]
                            clip_file = "%s%s%s%s%s.mp3" % \
                                (
                                    self.clip_dir,
                                    os.path.sep,
                                    actual_clip,
                                    os.path.sep,
                                    actual_clip
                                )
                            call(
                                "%s %s %s" % (
                                    self.play_cmd,
                                    clip_file,
                                    self.play_options,
                                ),
                                shell=True,
                            )
                            return True
        return False

    def __play_speech(self, text):
        parcel_index = 0
        text = text.replace("@COLON@", ":")
        if len(text) > self.google_translate_limit:
            char_count = 0
            index = 0
            parcel = []
            for word in text.split():
                char_count += len(word) + 1
                if char_count > self.google_translate_limit:
                    self.__get_speech_file(parcel, parcel_index)
                    parcel = [word]
                    char_count = len(word) + 1
                    parcel_index += 1
                else:
                    parcel.append(word)
                    index += 1
            self.__get_speech_file(parcel, parcel_index)
        else:
            self.__get_speech_file([text], parcel_index)
        call("cat /tmp/speech[0-9]*.mp3 > /tmp/speech.mp3", shell=True)
        call(
            "%s /tmp/speech.mp3 %s" % (
                self.play_cmd,
                self.play_options
            ),
            shell=True,
        )
        # It would look cleaner to do an os.remove() here, but this more easily
        # handles the filename wildcard, so fuck it
        call("rm -f /tmp/speech*.mp3", shell=True)
        return True

    def __get_speech_file(self, parcel, parcel_index):
        words = " ".join(parcel)
        headers = {'User-Agent': 'Mozilla'}
        url = "http://translate.google.com/translate_tts?ie=UTF-8" + \
            "&client=tw-ob&q=%s&tl=En-us" % words
        filename = "/tmp/speech%s.mp3" % parcel_index
        response = requests.get(url=url, headers=headers, stream=True)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)


if __name__ == "__main__":
    client = PoltergeistClient()
    client.start()
