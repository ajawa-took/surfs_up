# packages for analysis
import datetime as dt
import numpy as np
import pandas as pd

# package i hate for interacting with sqlite files/databases
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# package for building webpage
from flask import Flask, jsonify

# starting sqlalcheny code
engineBob = create_engine("sqlite:///hawaii.sqlite")
BaseBob = automap_base()
BaseBob.prepare(engineBob, reflect=True)

# in BaseBob.classes.measurement,
#  BaseBob is my variable, defined above
# .classes. is a keyword
# measurement is a table in the sqlite db
Measurement = BaseBob.classes.measurement
Station = BaseBob.classes.station

# sessionBob = Session(engineBob)


# webpage code
appBob = Flask(__name__)

@appBob.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! <br>
    Available Routes: <br>
    /api/v1.0/precipitation <br>
    /api/v1.0/stations <br>
    /api/v1.0/tobs <br>
    /api/v1.0/temp/start/end <br>
    ''')

# this application has a major problem:
# only one route using sqalchemy can be accessed without restarting flask
# reloading sqlalchemy-using page, or opening a second one throws
# sqlite3.ProgrammingError:
## SQLite objects created in a thread can only be used in that same thread.
## The object was created in thread id 39484 and this is thread id 40124.


@appBob.route("/api/v1.0/precipitation")
def precipitation():
    sessionBob = Session(engineBob)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipi_data = sessionBob.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    sessionBob.close()
    precip = {date: prcp for date, prcp in precipi_data}
    return jsonify(precip)

@appBob.route("/api/v1.0/stations")
def stations():
    sessionBob = Session(engineBob)
    results = sessionBob.query(Station.station).all()
    sessionBob.close()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@appBob.route("/api/v1.0/tobs")
def temp_monthly():
    sessionBob = Session(engineBob)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = sessionBob.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    sessionBob.close()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


@appBob.route("/api/v1.0/temp/<start>")
@appBob.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sessionBob = Session(engineBob)
    # print(f"start is {start} with type {type(start)}")
    # print(f"end is {end} with type {type(end)}")
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = sessionBob.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = sessionBob.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    sessionBob.close()
    temps = list(np.ravel(results))
    return jsonify(temps)






