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
    while len(clips) == 0 and time.time() - start_time < 30:
        for key in redis.scan_iter(target_key+":*"):
            clip = redis.get(key)
            if quiet or clip == "quiet":
                quiet = True
                clips = [ "quiet" ]
            else:
                clips.append(clip)
            redis.delete(key)
    return jsonify(clips = clips)


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
