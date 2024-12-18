from flask import Flask, jsonify, request, render_template
from models import db, PengajuanCuti
import redis
from rq import Queue
from rq.job import Job

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@db/sicuti'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

redis_conn = redis.StrictRedis(host='redis', port=6379, db=0)
queue = Queue(connection=redis_conn)

# @app.before_request
# def health_check():
#     try:
#         system_status = redis_conn.get('admin_service_status')

#         if system_status == b'inactive':
#             if request.endpoint == 'apply':
#                 return jsonify({"message": "Sistem pengajuan cuti sedang ditutup. Cuti tidak dapat diajukan."}), 403
#         redis_conn.set('admin_service_status', 'active', ex=60)
        
#     except Exception as e:
#         redis_conn.set('admin_service_status', 'inactive', ex=60)
#         print(f"Error while checking system status: {e}")


@app.route("/toggle_system", methods=["POST"])
def toggle_system():
    data = request.get_json()
    action = data.get("action")

    if action == "open":
        redis_conn.set('admin_service_status', 'active', ex=60)
        message = "Sistem pengajuan cuti dibuka!"
    elif action == "close":
        redis_conn.set('admin_service_status', 'inactive', ex=60)
        message = "Sistem pengajuan cuti ditutup!"
    else:
        message = "Tindakan tidak valid"

    return jsonify({"message": message})

@app.route('/check_status', methods=['GET'])
def check_status():
    try:
        # redis_conn.ping()
        admin_status = redis_conn.get('admin_service_status')

        if admin_status:
            redis_status = admin_status.decode('utf-8') 
        else:
            redis_status = 'inactive'

        return jsonify({"status": redis_status}), 200
    except redis.ConnectionError:
        return jsonify({"status": "inactive"}), 500



@app.route('/', methods=['GET', 'POST'])
def get_leave_requests():
    try:
        redis_conn.ping()
        redis_status = 'active'  # Redis aktif
    except redis.ConnectionError:
        redis_status = 'inactive'  # Redis tidak aktif

    if request.method == 'POST':
        data = request.get_json()

        pengajuan_id = data.get("id")
        action = data.get("action")
        pengajuan = PengajuanCuti.query.get_or_404(pengajuan_id)
        
        if action == 'approve':
            pengajuan.status = 'Disetujui'
            message = "Leave request approved!"
        elif action == 'reject':
            pengajuan.status = 'Ditolak'
            message = "Leave request rejected!"
        else:
            message = "Invalid action"

        db.session.commit()
        return jsonify({"message": message})

    data_cuti = PengajuanCuti.query.all()
    return render_template('home.html', data=data_cuti, redis_status=redis_status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')