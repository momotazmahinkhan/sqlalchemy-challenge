import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd


from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start<br/>"
        f"/api/v1.0/<Begin>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation """
    # Query all precipitation
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d') - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp, Measurement.station).\
                    filter (Measurement.date >query_date).all()

    session.close()

    # Convert list of tuples into normal list
    all_precipitation = list(np.ravel(results))

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

     # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_station = list(np.ravel(results))

    #Returns jsonified  
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the most active stations"""
    # Query the most active station and temperature 
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d') - dt.timedelta(days=365)
    results = session.query(Measurement.station, Measurement.tobs, Measurement.date ).\
        filter(Measurement.station == 'USC00519281').filter (Measurement.date >query_date).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    #Returns jsonified  
    return jsonify(all_tobs)

@app.route("/api/v1.0/start/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the min, max and avg temperature 
   
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    session.close()

    #Returns jsonified  
    return jsonify(results)

@app.route("/api/v1.0/<Begin>/<end>")
def begin_end(begin, end):
      
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the min, max and avg temperature 
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= begin).filter(Measurement.date <= end).all()
    session.close()

    #Returns jsonified  
    return jsonify(results)
    
if __name__ == '__main__':
    app.run(debug=True)
