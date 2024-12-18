from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, PengajuanCuti  # Pastikan models.py memiliki definisi model yang benar

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@db/sicuti'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def welcome():
    return render_template('home.html')


@app.route('/apply', methods=['GET'])
def apply_form():
    return render_template('apply_form.html')


@app.route('/apply', methods=['POST'])
def apply():
    try:
        data = request.get_json()
        nama = data.get('nama')
        alasan = data.get('alasan')

        pengajuan = PengajuanCuti(nama=nama, alasan=alasan)
        db.session.add(pengajuan)
        db.session.commit()

        return jsonify({"message": "Pengajuan berhasil dibuat"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Terdapat KEsalahan"}), 500

# Jalankan Aplikasi
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
