import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route('/')
def welcome():
    '''List all available api routes.'''
    return (
        f'<h3>Available Information:</h3><br/>'
        f'<a href=/api/v1.0/precipitation>Precipitation Data</a><br/>'
        f'<a href=/api/v1.0/stations>Station Data</a><br/>'
        f'<a href=/api/v1.0/tobs>Temperature Data</a><br/>'
        f'<a href=/api/v1.0/one>Min Avg and Max Temperature 2017-01-01 Forward</a><br/>'
        f'<a href=/api/v1.0/range>Min Avg and Max Temperature 2017-01-06 to 2017-31-12'
    )

@app.route('/api/v1.0/precipitation')
def rain():
    '''Return a list of dates and rain amounts'''
    # Query the dates and precipitation measurements from the last year.
    
    dates_precips = session.query(Measurement.date, 
                             Measurement.prcp
        ).filter(
         Measurement.date >= '2016-08-23'
        ).all()
    
    dict_dates = []
    dict_prcp = []

    for date, precip in dates_precips:
        dict_dates.append(date)
        dict_prcp.append(precip)

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    
    temp_dict = dict(zip(dict_dates, dict_prcp))
        
    return jsonify(temp_dict)

@app.route('/api/v1.0/stations')
def stations():
    '''Return a JSON list of stations from the dataset.'''
    # Query the station names from the station data.

    stations = session.query(Station).all()
    station_list = []

    for station in stations:
        station_dict = {}
        station_dict['Id'] = station.id
        station_dict['Name'] = station.name
        station_list.append(station_dict)
    
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def temps():
    '''Return a JSON list of Temperature Observations (tobs) for the previous year.'''
    #Query the temperature observations for the previous year.

    temps = session.query(Measurement).all()
    temp_list = []

    for temp in temps:
        temp_dict = {}
        temp_dict['Date'] = temp.date
        temp_dict['Temp Observed'] = temp.tobs
        temp_list.append(temp_dict)

    return jsonify(temp_list)

@app.route('/api/v1.0/one')
def one_date():
    '''Return a JSON list of the minimum, average, and maximum temperature for a given start date'''
    #Query all dates greater than and equal to the given start date.
    
    single_date = session.query(Measurement.date,
              func.min(Measurement.tobs), 
              func.avg(Measurement.tobs),
              func.max(Measurement.tobs)
        ).group_by(
            Measurement.date
        ).filter(
            Measurement.date >= '2017-01-01'
        ).all()

    single_list = []

    for row in single_date:
        single_dict = {}
        single_dict['Date'] = row[0]
        single_dict['Min'] = row[1]
        single_dict['Avg'] = row[2]
        single_dict['Max'] = row[3]
        single_list.append(single_dict)
    
    return jsonify(single_list)

@app.route('/api/v1.0/range')
def range_dates():
    '''Return a JSON list of the minimum, average, and maximum temperature for a range of dates'''
    #Query all dates between a given start and end date.

    range_date = session.query(Measurement.date,
              func.min(Measurement.tobs), 
              func.avg(Measurement.tobs),
              func.max(Measurement.tobs)
        ).group_by(
            Measurement.date
        ).filter(
            Measurement.date >= '2017-01-06'
        ).filter(
            Measurement.date <= '2017-31-12'
        ).all()

    range_list = []

    for row in range_date:
        range_dict = {}
        range_dict['Date'] = row[0]
        range_dict['Min'] = row[1]
        range_dict['Avg'] = row[2]
        range_dict['Max'] = row[3]
        range_list.append(range_dict)

    return jsonify(range_list)

if __name__ == '__main__':
    app.run(debug=True)