import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
hm = Base.classes.measurement
hs = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome_Hawaii_Temp_Data():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def Precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of prcp for 2016/08 to 2017/08"""
    # Query all passengers
    results = session.query(hm.date,hm.prcp).filter(hm.date >= '2016-08-01').all()

    session.close()

    # Convert list of tuples into normal list
    prcp_l = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_l.append(prcp_dict)


    return jsonify(prcp_l)

@app.route("/api/v1.0/station")
def Stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all
    results = session.query(hm.station.distinct()).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["Stations"] = station
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def Temperatures():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temps for one station"""
    # Query all
    results = session.query(hm.date,hm.tobs).filter(hm.station == 'USC00519281').filter(hm.date >= '2016-08-01').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_temp = []
    for tobs in results:
        temp_dict = {}
        temp_dict["USC00519281"] = tobs
        all_temp.append(temp_dict)

    return jsonify(all_temp)




if __name__ == '__main__':
    app.run(debug=False)
