# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Homepage<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/2016-08-22<br/>"
        f"/api/v1.0/temp/2013-08-22/2016-08-22"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    prcp_scores = ( 
        session.query(Measurement.date,Measurement.prcp).
        .filter(Measurement.date> "2016-08-23")
        .order_by(Measurement.date)
        .all()
    )
    session.close()

    prcp = dict(prcp_scores)
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations_tot = session.query(Station.name).all()
    session.close()

    totstations = list(np.ravel(stations_tot))
    return jsonify(totstations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    temps12_df = session.query(Measurement.tobs)\
            .filter(Measurement.station == 'USC00519281')\
            .filter(Measurement.date >= "2016-08-23").all()
    session.close()
    temp_data = list(np.ravel(tobs))

    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start = None, end = None):
    session = Session(engine)
    
    
    sel = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]

    if not end:
        tempresults = session.query(*sel).\
            filter(measurement.date >= start).all()
        temps = list(np.ravel(tempresults))
        return jsonify(temps)
    
    tempresults = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()

    tempres = list(np.ravel(tempresults))
    return jsonify(tempres)

if __name__ == "__main__":
    app.run(debug=True)

