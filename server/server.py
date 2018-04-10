import json, uuid, time
from redis import Redis
from flask import Flask, request, jsonify

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
    while len(clips) == 0:
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


@app.route('/', methods=['GET'])
def submit_command():
    domain = request.headers['Host']
    if domain.endswith("tv.inetu.org"):
        client_id = "inetu-hdmi19"
    elif domain.endswith("tv.inetu.net"):
        client_id = "inetu-hdmi13"
    else:
        return jsonify(status = "I couldn't find the client_id for the URL you requested"), 404
    target_key = '%s:clip:%s:%s' % (qkey, client_id, uuid.uuid4())
    clip_name = domain.split(".")[0]
    redis.set(target_key, clip_name)
    return jsonify(status = "Request to play %s on %s successfully queued" % (clip_name, client_id))


@app.route('/alexa', methods=['POST'])
def handle_alexa_request():
    print json.dumps(request.json, indent=2)
    return generate_response("Okay")


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
