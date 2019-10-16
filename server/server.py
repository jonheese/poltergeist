import json, uuid, time
from redis import Redis
from flask import Flask, request, jsonify, render_template
from jinja2 import TemplateNotFound
from datetime import datetime

app = Flask(__name__)

redis = Redis()
app.config['REDIS_QUEUE_KEY'] = 'poltergeist'
qkey = app.config['REDIS_QUEUE_KEY']


@app.route('/cmd/<client_id>', methods=['GET'])
def get_commands(client_id):
    target_key = '%s:clip:%s' % (qkey, client_id)
    clips = []
    start_time = time.time()
    while len(clips) == 0 and time.time() - start_time < 60:
        for key in redis.scan_iter(target_key+":*"):
            clip = redis.get(key)
            clips.append(clip)
            if clip.startswith("quiet:") or clip.startswith("quiet_all:"):
                clips = [ clip ]
                break
        time.sleep(0.05)
    return json.dumps({"clips": clips})


@app.route('/delete/<key>', methods=['GET'])
def delete(key):
    redis.delete(key)
    return "Success deleting key %s" % key


@app.route('/monitor', methods=['GET'])
def monitor():
    return "Success"


@app.route('/robots.txt', methods=['GET'])
def robots():
    return "User agent: * \n" + \
           "Disallow: /"


@app.route('/play/<clip_name>', methods=['GET'])
@app.route('/', methods=['GET'])
def submit_command(clip_name=None):
    try:
        user_agent = request.headers['User-Agent'].lower()
        if "bot" in user_agent and not user_agent.startswith("slackbot"):
            return ""
    except KeyError:
        return ""

    domain = request.headers['Host']
    if domain.endswith("inetu.net"):
        client_id = "inetu-hdmi13"
    elif domain.endswith("inetu.org") or domain.endswith("jonheese.com"):
        client_id = "inetu-hdmi19"
    else:
        return jsonify(status = "I couldn't find the client_id for the URL you requested"), 404

    if not clip_name:
        clip_name = domain.split(".")[0]

    if (clip_name.lower() == "friday" and datetime.today().weekday() != 4) or \
            ((clip_name.lower() == "lastchristmas" or clip_name.lower() == "jinglebell") and datetime.today().month != 12) or \
            (clip_name.lower() == "mondays" and datetime.today().weekday() != 0):
        return '<html><body><p align="center"><img src="/static/stahp.jpg" /></p></body></html>'
    put_command(client_id, clip_name)

    try:
        return render_template('%s/index.html' % clip_name)
    except TemplateNotFound:
        return render_template("notfound.html")


def put_command(client_id, clip_name):
    timestamp = time.time()
    target_key = '%s:clip:%s:%s' % (qkey, client_id, timestamp)
    redis.set(target_key, "%s:%s" % (clip_name, str(timestamp)))


@app.route('/alexa', methods=['POST'])
def handle_alexa_request():
    print json.dumps(request.json, indent=2)
    data = request.json
    request_type = data["request"]["type"]
    if request_type == "IntentRequest":
        clip_name = data["request"]["intent"]["slots"]["clip"]["value"].replace(" ", "").lower()
        put_command("inetu-hdmi19", clip_name)
        return generate_response("Okay")
    else:
        return generate_response("I couldn't find that clip")


def generate_response(output_speech, card_title="", card_subtitle="", card_content="", endSession=True):
    response = {
        "version": "1.0",
        "sessionAttributes": {
            "user": {
                "name": "Jon Heese"
            }
        },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": output_speech
            },
            "card": {
                "type": "Simple",
                "title": card_title,
                "subtitle": card_subtitle,
                "content": card_content
            },
            "shouldEndSession": endSession
        }
    }
    return json.dumps(response)
