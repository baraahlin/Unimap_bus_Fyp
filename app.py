# app.py
import os
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from sqlalchemy import text
app = Flask(__name__)
app._static_folder = 'templates/static'
#app.add_url_rule('/photos/img')
#app._static_folder = os.path.abspath("static/")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ulvd21skdi?25B@localhost/new_schema'  # Replace with your MySQL connection details
db = SQLAlchemy(app)


#cursor = db.cursor(dictionary=True)
'''
@app.route('/static/js/StuDash.js')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static', 'js'),   filename)
'''
#to open the pages
@app.route('/')
def home():
    return render_template('MainFile.html')

@app.route('/AdminDashboard')
def admin():
    return render_template('AdminDashboard.html')

@app.route('/DriverDashboard')
def driver():
    return redirect('/get_on_service_info')
    return render_template('DriverDashboard.html')

@app.route('/StudentDashboard')
def student():
    return render_template('StudentDashboard.html')

@app.route('/BusInformation')
def bus_info():
    return render_template('BusInformation.html')

@app.route('/DriverInformation')
def driver_info():
    return render_template('DriverInformation.html')

@app.route('/BusRequest')
def bus_requests():
    return render_template('BusRequest.html')

@app.route('/Destination')
def destination():
    return render_template('Destination.html')

#to write and get data from the database
#to write and read driver information, for table driver , DriverInformation Page

class Drivers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    staff_no = db.Column(db.Integer, nullable=False)

@app.route('/submit_driver_info', methods=['GET', 'POST'])
def send_driver_info():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = int(request.form['age'])
        staff_no = int(request.form['staff_no'])

        profile = Drivers(first_name=first_name, last_name=last_name, age=age, staff_no=staff_no)
        db.session.add(profile)
        db.session.commit()

    profiles = Drivers.query.all()
    return redirect('/get_driver_info')
    return render_template('DriverInformation.html')

@app.route('/get_driver_info', methods=['GET', 'POST'])
def get_driver_info():
    query = text('SELECT * FROM new_schema.drivers')
    profiles = db.session.execute(query).fetchall()
    profiles = Drivers.query.all() 
    return render_template('DriverInformation.html', profiles=profiles)
    return render_template('Try.html')



class OnServices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(50), nullable=False)
    bus_number = db.Column(db.Integer, nullable=False)
    destination_name = db.Column(db.String(20), nullable=False)
    driver_latitude = db.Column(db.Float, nullable=False)
    driver_longitude = db.Column(db.Float, nullable=False)


@app.route('/submit_info', methods=['GET','POST'])
def submit_info():
    driver_name = request.form.get('driver_name')
    bus_number = request.form.get('bus_number')
    destination_name = request.form.get('destination_name')
    driver_latitude = request.form.get('latitude')
    driver_longitude = request.form.get('longitude')

    # Validate and convert bus_number to integer
    if bus_number is not None:
        try:
            bus_number = int(bus_number)
        except ValueError:
            return jsonify({"error": "bus_number must be an integer"}), 400
    
    # Check if required form data is present
    if not driver_name or bus_number is None or not destination_name:
        return jsonify({"error": "Missing form data"}), 400
    print(f"driver_name: {driver_name}, bus_number: {bus_number}, destination_name: {destination_name}, latitude: {driver_latitude}, longitude: {driver_longitude}")

    # Create a new service entry
    new_service = OnServices(
        driver_name=driver_name,
        bus_number=bus_number,
        destination_name=destination_name,
        driver_latitude=driver_latitude,
        driver_longitude=driver_longitude
    )
    
    # Add to the session and commit to the database
    db.session.add(new_service)
    db.session.commit()
    
    return redirect('/get_on_service_info')

@app.route('/get_on_service_info', methods=['Get','POST'])

def get_on_service_info():
    driver_names = Drivers.query.with_entities(Drivers.first_name).all()
    bus_numbers = Buses.query.with_entities(Buses.bus_number).all()
    destinations = Destinations.query.with_entities(Destinations.destination_name).all()
    #return redirect('/submit_info')
    return render_template('DriverDashboard.html', driver_names=driver_names, bus_numbers=bus_numbers, destinations=destinations)

@app.route('/display_service_info', methods=['GET', 'POST'])
def display_service_info():
    query = text('SELECT * FROM new_schema.on_services')
    services = db.session.execute(query).fetchall()
    services = OnServices.query.all()
    return render_template('AdminDashboard.html', services=services)

@app.route('/display_service_info_student', methods=['GET', 'POST'])
def display_service_info_student():
    query = text('SELECT * FROM new_schema.on_services')
    services = db.session.execute(query).fetchall()
    services = OnServices.query.all()
    #return redirect('/StudentDashboard')
    return render_template('StudentDashboard.html', services=services)

@app.route('/display_service_info_student_stu', methods=['GET', 'POST'])
def display_service_info_student_stu():
    query = text('SELECT * FROM new_schema.on_services')
    destinations = Destinations.query.with_entities(Destinations.destination_name).all()
    services = db.session.execute(query).fetchall()
    services = OnServices.query.all()
    #return redirect('/StudentDashboard')
    return render_template('StudentDashboard.html', services=services, destinations=destinations)


#to write and read bus information, for buses table, BusInformation file

class Buses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bus_number = db.Column(db.Integer, nullable=False)
    number_plate = db.Column(db.String(20), nullable=False)
    bus_capacity = db.Column(db.Integer, nullable=False)
    bus_status = db.Column(db.String(20), nullable=False)

@app.route('/submit_bus_info', methods=['GET', 'POST'])
def send_bus_info():
    if request.method == "POST":
        bus_number = int(request.form['bus_number'])
        number_plate = request.form['number_plate']
        bus_capacity = int(request.form['bus_capacity'])
        #bus_status = request.form['bus_status']

        bus = Buses(bus_number=bus_number, number_plate=number_plate, bus_capacity=bus_capacity)
        db.session.add(bus)
        db.session.commit()

    buses = Buses.query.all()
    return redirect('/get_bus_info')

@app.route('/get_bus_info', methods=['GET', 'POST'])
def get_bus_info():
    query = text('SELECT * FROM new_schema.buses')
    buses = db.session.execute(query).fetchall()
    buses = Buses.query.all()
    return render_template('BusInformation.html', buses=buses)

#to write and read destination information, for destination table, 
# Destination file

class Destinations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_name = db.Column(db.String(20), nullable=False)
    des_latitude = db.Column(db.Integer, nullable=False)
    des_longitude = db.Column(db.Integer, nullable=False)

@app.route('/submit_destination', methods=['GET', 'POST'])
def send_destination():
    if request.method == "POST":
        destination_name = request.form['destination_name']
        des_latitude = float(request.form['des_latitude'])
        des_longitude = float(request.form['des_longitude'])

        destination = Destinations(destination_name=destination_name, des_latitude=des_latitude, des_longitude=des_longitude)
        db.session.add(destination)
        db.session.commit()

    destinations = Destinations.query.all()
    return redirect('/get_destination')

@app.route('/get_destination', methods=['GET', 'POST'])
def get_destination():
    query = text('SELECT * FROM new_schema.destinations')
    destinations = db.session.execute(query).fetchall()
    destinations = Destinations.query.all()
    return render_template('Destination.html', destinations=destinations)


#write and read book bus information , from 
# StudentDashboard to BusRequests

class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_location = db.Column(db.String(20), nullable=False)
    end_location = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)

@app.route('/submit_booking', methods=['GET', 'POST'])
def send_requests():
    if request.method == "POST":
        start_location = request.form['start_location']
        end_location = request.form['end_location']
        date = request.form['date']
        time = request.form['time']

        bus_request = Requests(start_location=start_location, end_location=end_location, date=date, time=time)
        db.session.add(bus_request)
        db.session.commit()

    requests = Requests.query.all()
    return redirect('/StudentDashboard')

@app.route('/get_requests', methods=['GET', 'POST'])
def get_requests():
    query = text('SELECT * FROM new_schema.requests')
    bus_requests = db.session.execute(query).fetchall()
    bus_requests = Requests.query.all()
    return render_template('BusRequest.html', bus_requests=bus_requests)

@app.route('/get_destination_list', methods=['GET', 'POST'])
def get_destination_list():
    query = text('SELECT destination_name FROM new_schema.destinations')
    bus_destination_list = db.session.execute(query).fetchall()
    bus_destination_list = Destinations.query.all()
    return render_template('StudentDashboard.html', bus_destination_list=bus_destination_list)
# driver dashboard to student dashboard 
'''
class Services(db.Model):
    id = the normall increment
    destination = //driver distination 
    bus_num = driver bus 
    eta = calculate 

@app.route('/get_on_service', methods=['GET', 'POST'])
def get_on_service():
    query = text('SELECT * FROM new_schema.services')
    services = db.session.execute(query).fetchAll()
    services = Services.query.all()
    return render_template('StudentDashboard.html', services=services)

'''
if __name__ == '__main__':
    app.run(debug=True)
