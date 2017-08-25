#!/usr/bin/env python3
import datetime
import json
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('db.labs')
db = client.tracking
coll = db.timeseries


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        request.json['tstamp'] = datetime.datetime.utcnow()
        print(request.json)
        coll.insert(request.json)
        return ''

    return 'Hello!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4567)
