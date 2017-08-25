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
        if 'location' not in data:
            # I do not care about points with no location
            return ''
        data['geopoint'] = {'type': 'Point',
                            'coordinates':
                                [
                                    data['location']['LONG'],
                                    data['location']['LAT']
                                ]
                            }
        cur_state.update({"ID": data["ID"]}, request.json, upsert=True)
        coll.insert(request.json)
        return ''

    return 'Hello!'

@app.route('/track/<string:phone_id>')
def track(phone_id):
    three_hours = datetime.datetime.utcnow() - datetime.timedelta(seconds=3*3600)
    ret = track(phone_id, three_hours)
    linestring = data_to_linestring(ret)
    filtered = filter_close(linestring, 0.0000003)

    return jsonify({'ls': filtered, 'ret':ret})


@app.route('/state/<string:phone_id>')
def state(phone_id):
    res = cur_state.find({"ID": phone_id}, {'_id': 0})
    try:
        ret = next(res)
    except Exception as e:
        print(e)
        ret = {}
    return jsonify(ret)


def fixts(item):
    item['tstamp'] = item['tstamp'].timestamp()
    return item


def track(phone_id, since):
    res = coll.find({'ID': phone_id,
                     'tstamp': {'$gte': since}},
                    {'location.LAT': 1, 'location.LONG': 1, 'tstamp': 1, '_id': 0})
    res.sort('tstamp', -1)
    ret = list(map(fixts, res))
    return ret


def distance(p, q):
    d = (p[0]-q[0])**2 + (p[1]-q[1])**2
    return d


def filter_close(points, dst):
    ret = [points[0]]
    for idx in range(len(points) - 1):
        if distance(ret[-1], points[idx]) > dst:
            ret.append(points[idx])
    return ret


def data_to_linestring(data):
    return list(map(lambda x: [x['location']['LAT'], x['location']['LONG']], data))


if __name__ == '__main__':
    # six_hours = datetime.datetime.today() - datetime.timedelta(seconds=6*3600)
    # l = track("", six_hours)
    # l = track("", six_hours)
    # data = data_to_linestring(l)
    # print(len(data))
    # filtered = filter_close(data, 0.0000003)
    # print(filtered)
    # print(len(filtered))
    app.run(host="0.0.0.0", port=4567, debug=True)
