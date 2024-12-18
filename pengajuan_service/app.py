from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import redis
from rq import Queue
from models import db, PengajuanCuti  # Pastikan models.py memiliki definisi model yang benar

app = Flask(__name__)

# Konfigurasi database MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@db/sicuti'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi database
db.init_app(app)

# Inisialisasi Redis dan Queue
redis_conn = redis.StrictRedis(host='redis', port=6379, db=0)  # Koneksi ke Redis service yang ada di docker-compose
queue = Queue(connection=redis_conn)  # Membuat queue untuk menambahkan task ke Redis

with app.app_context():
    db.create_all()


def check_admin_service_status():
    status = redis_conn.get('admin_service_status')
    if status is None or status.decode() != 'active':
        return False
    return True

@app.route('/', methods=['GET'])
def welcome():
    return render_template('home.html')


@app.route('/apply', methods=['GET'])
def apply_form():
    return render_template('apply_form.html')


@app.route('/apply', methods=['POST'])
def apply():
    try:
        if not check_admin_service_status():
            return jsonify({"message": "Service validasi sedang tidak tersedia. Silakan coba beberapa saat lagi."}), 503
            
        data = request.get_json()
        nama = data.get('nama')
        alasan = data.get('alasan')

        # Simpan pengajuan cuti ke database
        pengajuan = PengajuanCuti(nama=nama, alasan=alasan)
        db.session.add(pengajuan)
        db.session.commit()

        # Setelah pengajuan cuti berhasil, kirimkan task ke Redis untuk validasi
        # Misalnya task ini memanggil fungsi validasi yang ada di service admin
        job = queue.enqueue('validasi_service.process_validasi', pengajuan.id)

        return jsonify({"message": "Pengajuan berhasil dibuat, sedang diproses!"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Terdapat Kesalahan"}), 500


# Jalankan Aplikasi
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
