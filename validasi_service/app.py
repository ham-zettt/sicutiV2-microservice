from flask import Flask, jsonify, request, render_template
from models import db, LeaveRequest

app = Flask(__name__)

# Konfigurasi database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@db/sicuti'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/approve/<int:id>', methods=['PUT'])
def approve_leave(id):
    leave_request = LeaveRequest.query.get_or_404(id)
    leave_request.status = 'Approved'
    db.session.commit()
    return jsonify({"message": "Leave request approved!"})

@app.route('/reject/<int:id>', methods=['PUT'])
def reject_leave(id):
    leave_request = LeaveRequest.query.get_or_404(id)
    leave_request.status = 'Rejected'
    db.session.commit()
    return jsonify({"message": "Leave request rejected!"})

@app.route('/', methods=['GET'])
def get_leave_requests():
    data_cuti = LeaveRequest.query.all()
    return render_template('home.html', data=data_cuti)
    # return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')