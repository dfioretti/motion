from flask import jsonify, render_template, request
from app import app
from flask.ext.pymongo import PyMongo
import datetime
import pytz

mongo = PyMongo(app)
utc=pytz.UTC


@app.route('/')
@app.route('/index')
def index():
    #app = Flask(__name__)
    #mongo = PyMongo(app)
    #data = mongo.db.sensor.insert({"test" : "yes"})#.findOne()#({'online': True})
    #return "OK"#data['test']
    return render_template('index.html')

@app.route('/status')
def status():
    #record = mongo.db.sensor.find().limit(1).sort({'$natural':-1})
    record = mongo.db.sensor.find({}).sort("_id", -1).limit(1)[0]
    #old = utc.localize(record['updated_at'])
    old = record['updated_at']
    new = utc.localize(datetime.datetime.now())
    difference = (new - old).seconds
    ret_data = {}
    if (difference > 240):
        ret_data['value'] = True
    else:
        ret_data['value'] = False
    return jsonify(ret_data)
    #return str(difference)
    #return record['updated_at'].strftime('%m/%d/%Y')
    #return { "active" : true }

@app.route('/update')
def update():
    new_update = { 'update' : 'yes', 'updated_at' : datetime.datetime.now() }
    mongo.db.sensor.insert( new_update )
    return "UPDATED"
