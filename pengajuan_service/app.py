from flask import Flask, request, jsonify, render_template
from models import db, PengajuanCuti

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@db/sicuti'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET'])
def welcome():
    return render_template('home.html')


@app.route('/apply_form', methods=['GET'])
def apply_leave_form():
    return render_template('apply_form.html')


@app.route('/apply', methods=['POST'])
def apply():
    nama = request.form.get('nama')
    alasan = request.form.get('alasan')

    pengajuan = PengajuanCuti(nama=nama, alasan=alasan)
    db.session.add(pengajuan)
    db.session.commit()

    return jsonify({"message": "Leave application submitted successfully!"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')