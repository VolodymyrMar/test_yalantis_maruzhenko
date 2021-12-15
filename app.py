from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from time import time
from time_utils import timestamp_to_output, input_to_timestamp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    created_at = db.Column(db.Integer, default=round(time()))
    updated_at = db.Column(db.Integer, default=round(time()))

    def __repr__(self):
        return '<Driver %r>' % self.id


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String())
    model = db.Column(db.String)
    plate_number = db.Column(db.String)
    created_at = db.Column(db.Integer, default=round(time()))
    updated_at = db.Column(db.Integer, default=round(time()))

    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))


@app.route('/')
def index():
    return 'Hello World'


@app.route('/drivers/driver/', methods=['GET', 'POST'])
def get_drivers():
    if request.method == "POST":
        driver = Driver(first_name=request.json['first_name'],
                        last_name=request.json['last_name'])
        try:
            db.session.add(driver)
            db.session.commit()
            return {'status': 'OK'}
        except:
            return {'status': 'Error'}
    else:
        no_args = False
        is_before = None
        if request.args.get('created_at__gte'):
            is_before = False
        elif request.args.get('created_at__lte'):
            is_before = True
        else:
            no_args = True
        return {'drivers': [
            {
                'id': driver.id,
                'name': driver.first_name,
                'surname': driver.last_name,
                'created_at': timestamp_to_output(driver.created_at),
                'updated_at': timestamp_to_output(driver.updated_at),
            }
            for driver in Driver.query.all()
            if no_args or
            (driver.created_at > input_to_timestamp(request.args.get(not is_before
            and f'created_at__gte' or 'created_at__lte'))) ^ is_before
        ]}


@app.route('/drivers/driver/<driver_id>', methods=['GET', 'DELETE', 'UPDATE'])
def change_driver(driver_id):
    driver = Driver.query.get(driver_id)
    if request.method == "GET":
        return {
            'id': driver.id,
            'name': driver.first_name,
            'surname': driver.last_name,
            'created_at': timestamp_to_output(driver.created_at),
            'updated_at': timestamp_to_output(driver.updated_at),
        }
    elif request.method == 'DELETE':
        try:
            db.session.delete(driver)
            db.session.commit()
            return {'status': 'OK DELETE'}
        except:
            return {'status': 'Error DELETE'}
    else:
        driver.first_name = request.json['first_name']
        driver.last_name = request.json['last_name']
        try:
            db.session.commit()
            return {'status': 'OK'}
        except:
            return {'status': 'Error'}


@app.route('/vehicles/vehicle/', methods=['POST', 'GET'])
def vehicle():
    args = request.args
    if request.method == 'POST':
        vehicle = Vehicle(make=request.json['make'],
                          model=request.json['model'],
                          plate_number=request.json['plate_number'],
                          driver_id=request.json['driver_id'])
        try:
            db.session.add(vehicle)
            db.session.commit()
            return {'status': 'OK'}
        except:
            return {'status': 'Error'}
    else:
        no_args = False
        with_driver = None
        if args.get('with_drivers') == 'yes':
            with_driver = True
        elif args.get('with_drivers') == 'no':
            with_driver = False
        else:
            no_args = True
        return {'vehicles': [
            {
                'id': car.id,
                'make': car.make,
                'model': car.model,
                'plate_number': car.plate_number,
                'created_at': timestamp_to_output(car.created_at),
                'updated_at': timestamp_to_output(car.updated_at),
                'driver_id': car.driver_id,
            }
            for car in Vehicle.query.all()
            if no_args or
               (car.driver_id == None) ^ with_driver
        ]}


@app.route('/vehicles/vehicle/<vehicle_id>', methods=['GET', 'POST', 'UPDATE', 'DELETE'])
def change_vehicle(vehicle_id):
    car = Vehicle.query.get(vehicle_id)
    if request.method == 'GET':
        return {
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'plate_number': car.plate_number,
            'created_at': timestamp_to_output(car.created_at),
            'updated_at': timestamp_to_output(car.updated_at),
            'driver_id': car.driver_id,
        }
    elif request.method == 'DELETE':
        try:
            db.session.delete(car)
            db.session.commit()
            return {'status': 'OK DELETE'}
        except:
            return {'status': 'Error DELETE'}
    elif request.method == 'UPDATE':
        car.make = request.json['make']
        car.model = request.json['model']
        car.plate_number = request.json['plate_number']
        try:
            db.session.commit()
            return {'status': 'OK'}
        except:
            return {'status': 'Error'}
    else:
        car.driver_id = request.json['driver_id']
        try:
            db.session.commit()
            return {'status': 'OK'}
        except:
            return {'status': 'Error'}


if __name__ == '__main__':
    app.run(debug=True)
