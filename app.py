#!/usr/bin/env python3
import datetime
import json
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('db.labs')
db = client.tracking
coll = db.timeseries
cur_state = db.cur_state


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        request.json['tstamp'] = datetime.datetime.utcnow()
        data = request.json
        print(data)
        cur_state.update({"ID": data["ID"]}, request.json, {'upsert': True})
        coll.insert(request.json)
        return ''

    return 'Hello!'

@app.route('/track/<string:phone_id>')
def track(phone_id):
    print(phone_id)
    yesterday = datetime.datetime.today() - datetime.timedelta(seconds=6*3600)
    print(yesterday)
    res = coll.find({'ID': phone_id,
                     'tstamp': {'$gte': yesterday}},
                    {'location.LAT': 1, 'location.LONG': 1, 'tstamp': 1, '_id': 0})
    res.sort('tstamp', -1)
    ret = list(map(fixts, res))

    return jsonify({'ret':ret})


@app.route('/state/<string:phone_id>')
def state(phone_id):
    res = cur_state.find({"ID": phone_id}, {'_id': 0})
    try:
        ret = res.next()
    except:
        ret = {}
    return jsonify(ret)


def fixts(item):
    item['tstamp'] = item['tstamp'].timestamp()
    return item


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4567, debug=True)
