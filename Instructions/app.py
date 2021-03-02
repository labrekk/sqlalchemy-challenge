import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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

@app.route("/")
def index():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        "/api/v1.0/{start}<br/>"
        "/api/v1.0/{start}/{end}"
    )
#   * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

#   * Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    temps = []

    for date, prcp in results:
        weather_dict = {}
        weather_dict['date'] = date
        weather_dict['prcp'] = prcp
        temps.append(weather_dict)
    
    return jsonify(temps)
#   * Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()

    session.close()

    station_names = list(np.ravel(results))

    return jsonify(station_names)

#   * Query the dates and temperature observations of the most active station for the last year of data.

#   * Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    one_year_data = dt.date(2017, 8, 23) - dt.timedelta(days=365)
#station ID pulled from ipynb 
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_data).filter(Measurement.station == 'USC00519281').order_by(Measurement.date.desc()).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    mintemp = func.min(Measurement.tobs)
    maxtemp = func.max(Measurement.tobs)
    avgtemp = func.avg(Measurement.tobs)

    results = session.query(mintemp, maxtemp, avgtemp).filter(Measurement.date >= start).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def end(start,end):
    session = Session(engine)

    mintemp = func.min(Measurement.tobs)
    maxtemp = func.max(Measurement.tobs)
    avgtemp = func.avg(Measurement.tobs)

    results = session.query(mintemp, maxtemp, avgtemp).filter(Measurement.date >= start).filter(Measurement.date < end).all()

    session.close()

    return jsonify(results)



if __name__ == '__main__':
    app.run(debug=True)



