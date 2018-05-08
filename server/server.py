import json, uuid, time
from redis import Redis
from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

redis = Redis()
app.config['REDIS_QUEUE_KEY'] = 'poltergeist'
qkey = app.config['REDIS_QUEUE_KEY']

@app.route('/cmd/<client_id>', methods=['GET'])
def get_commands(client_id):
    target_key = '%s:clip:%s' % (qkey, client_id)
    clips = []
    quiet = False
    start_time = time.time()
    while len(clips) == 0 and time.time() - start_time < 600:
        for key in redis.scan_iter(target_key+":*"):
            clip = redis.get(key)
            if quiet or clip == "quiet":
                quiet = True
                clips = [ "quiet" ]
            else:
                clips.append(clip)
            redis.delete(key)
        time.sleep(0.05)
    return json.dumps({"clips": clips})


@app.route('/monitor', methods=['GET'])
def monitor():
    return "Success"


@app.route('/', methods=['GET'])
def submit_command():
    user_agent = request.headers['User-Agent'].lower()
    if "bot" in user_agent:
        return ""

    domain = request.headers['Host']
    if domain.endswith("inetu.org"):
        client_id = "inetu-hdmi19"
    elif domain.endswith("inetu.net"):
        client_id = "inetu-hdmi13"
    else:
        return jsonify(status = "I couldn't find the client_id for the URL you requested"), 404
    clip_name = domain.split(".")[0]

    if (clip_name.lower() == "friday" and datetime.today().weekday() != 4) or \
            (clip_name.lower() == "lastchristmas" and datetime.today().month != 12) or \
            (clip_name.lower() == "jinglebell" and datetime.today().month != 12):
        return '<html><body><p align="center"><img src="/static/stahp.jpg" /></p></body></html>'
    put_command(client_id, clip_name)

    return render_template('%s/index.html' % clip_name)
    #return urllib2.urlopen("http://tv-static.inetu.org/%s" % clip_name).read()
    #return jsonify(status = "Request to play %s on %s successfully queued" % (clip_name, client_id))


def put_command(client_id, clip_name):
    target_key = '%s:clip:%s:%s' % (qkey, client_id, uuid.uuid4())
    redis.set(target_key, clip_name)


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
