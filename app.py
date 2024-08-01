from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:12345@db:5432/smarthome'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model for smart home data
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Device {self.name}>'

# Initialize database
with app.app_context():
    db.create_all()

# Route to get all devices
@app.route('/devices', methods=['GET'])
def get_devices():
    devices = Device.query.all()
    return jsonify([{'id': d.id, 'name': d.name, 'status': d.status} for d in devices])

# Route to add a new device
@app.route('/devices', methods=['POST'])
def add_device():
    if not request.json or 'name' not in request.json or 'status' not in request.json:
        abort(400, description="Invalid input")
        
    data = request.get_json()
    new_device = Device(name=data['name'], status=data['status'])
    
    try:
        db.session.add(new_device)
        db.session.commit()
        return jsonify({'id': new_device.id, 'name': new_device.name, 'status': new_device.status}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Device already exists'}), 400

# Route to update device status
@app.route('/devices/<int:id>', methods=['PUT'])
def update_device(id):
    if not request.json or 'status' not in request.json:
        abort(400, description="Invalid input")
        
    device = Device.query.get_or_404(id)
    device.status = request.json['status']
    db.session.commit()
    return jsonify({'id': device.id, 'name': device.name, 'status': device.status})

# Route to delete a device
@app.route('/devices/<int:id>', methods=['DELETE'])
def delete_device(id):
    device = Device.query.get_or_404(id)
    db.session.delete(device)
    db.session.commit()
    return jsonify({'message': 'Device deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
